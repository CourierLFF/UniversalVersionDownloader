import requests
from bs4 import BeautifulSoup
import re
import os


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










