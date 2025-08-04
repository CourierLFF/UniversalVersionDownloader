import requests
from bs4 import BeautifulSoup
import re
import os
import subprocess
import shutil


def forge_download(versions):
    for version in versions:
        print("Downloading Forge Files HTML")
        forge_files_url = f"https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html"
        forge_files_html = ""
        latest_forge_version = ""

        try:
            response = requests.get(forge_files_url)
            response.raise_for_status()

            forge_files_html = response.text

            print("Forge Files HTML Downloaded Successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading Forge Files HTML, invalid version: {e}")
            continue


        soup = BeautifulSoup(forge_files_html, "html.parser")

        description_tag = soup.find("meta", property="og:description")

        match = re.search(r'Latest:\s*([\d.]+)', description_tag.get("content"))
        if match:
            latest_forge_version = match.group(1)
            print(f"Latest Version: {latest_forge_version}")
        else:
            print(f"Cannot find latest forge version for {version}")
            continue

        version_download_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{latest_forge_version}/forge-{version}-{latest_forge_version}-installer.jar"
        output_dir = os.path.join("versions/forge", version)
        output_file = os.path.join(output_dir, f"{version}.jar")
        os.makedirs(output_dir, exist_ok=True)

        try:
            response = requests.get(version_download_url, stream=True)
            response.raise_for_status()

            print("Downloading Forge " + version + " Installer file")
            with open(output_file, "wb") as file:
                for chunk in response.iter_content(8192):
                    file.write(chunk)
            print("Version installer downloaded successfully to " + output_dir)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading version installer: {e}")
            continue

        if not os.path.isdir(output_dir):
            print(f"Error: Directory {output_dir} does not exist")
            continue
        else:
            try:
                print(f"Installing Forge {version} server... (May take a few moments)")
                result = subprocess.run(["java", "-jar", f"{version}.jar", "--installServer"], cwd=output_dir, capture_output=True, text=True, check=True)
                print(f"Forge {version} server installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"Stderr: {e.stderr}")

        split_version = version.split(".")
        if int(split_version[1]) <= 16:

            print("Cleaning Forge installed files")
            for item_name in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item_name)
                if item_name.endswith(".log") or item_name.startswith(f"{version}"):
                    os.remove(item_path)
            print("Cleaned NeoForge installed files successfully")

            print("Renaming Forge server jar")
            for item_name in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item_name)
                if item_name.startswith("forge"):
                    os.rename(item_path, os.path.join(output_dir, "server.jar"))
            print("Renamed Forge server jar successfully")

        elif int(split_version[1]) <= 20:
            pass
        else:
            pass










