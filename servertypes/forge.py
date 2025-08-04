import requests
from bs4 import BeautifulSoup
import re
import os
import subprocess
import shutil


def forge_download(versions):
    for version in versions:
        # Forge does not have any kind of easy API or simple URL scheme for finding versions and downloading them. So instead the HTML of the website is scraped to find the latest version of forge for the selected Minecraft version and then a URL is formed from it.
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

        # Parsing the HTML to find the meta description tag in the head. This tag contains the lastest version of the selected Minecraft version.
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
        # For some reason random versions use a different URL scheme, 1.7.10 seems to be the most popular version that uses a different URL scheme, so I'll just hardcode it in for now until I come up with a better solution.
        if version == "1.7.10":
            version_download_url = "https://maven.minecraftforge.net/net/minecraftforge/forge/1.7.10-10.13.4.1614-1.7.10/forge-1.7.10-10.13.4.1614-1.7.10-installer.jar"
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

        # Forge versions have changed a bit throughout all their versions, different files are required to be renamed and kept inside the server files for the version to boot properly.
        # Forge Version < 16 needs server.jar rename from forge jar
        # Forge Version <= 1.20.2 and > 16 needs libraries folder
        # Forge Version > 1.20.2 needs shim renamed and libraries folder
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

            print("Creating EULA file")
            eula_dir = os.path.join(output_dir, "eula.txt")
            with open(eula_dir, "w") as file:
                file.write("eula=true")
            print("Created EULA file successfully")

            print("Zipping files")
            shutil.make_archive(f"{version}", "zip", output_dir)
            shutil.move(f"{version}.zip", output_dir)
            print("Finished zipping files")

        elif int(split_version[1]) <= 20 and int(split_version[2]) <= 2:

            print("Cleaning Forge installed files")
            for item_name in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item_name)
                if os.path.isfile(item_path):
                    os.remove(item_path)
            print("Cleaned NeoForge installed files successfully")

            print("Creating EULA file")
            eula_dir = os.path.join(output_dir, "eula.txt")
            with open(eula_dir, "w") as file:
                file.write("eula=true")
            print("Created EULA file successfully")

            print("Zipping files")
            shutil.make_archive(f"{version}", "zip", output_dir)
            shutil.move(f"{version}.zip", output_dir)
            print("Finished zipping files")

        else:
            print("Cleaning Forge installed files")
            for item_name in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item_name)
                if os.path.isfile(item_path) and not "shim" in item_name:
                    os.remove(item_path)
            print("Cleaned NeoForge installed files successfully")

            print("Renaming Forge server jar")
            for item_name in os.listdir(output_dir):
                item_path = os.path.join(output_dir, item_name)
                if "shim" in item_name:
                    os.rename(item_path, os.path.join(output_dir, "server.jar"))
            print("Renamed Forge server jar successfully")

            print("Creating EULA file")
            eula_dir = os.path.join(output_dir, "eula.txt")
            with open(eula_dir, "w") as file:
                file.write("eula=true")
            print("Created EULA file successfully")

            print("Zipping files")
            shutil.make_archive(f"{version}", "zip", output_dir)
            shutil.move(f"{version}.zip", output_dir)
            print("Finished zipping files")










