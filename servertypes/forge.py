import requests
from bs4 import BeautifulSoup
import re


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








