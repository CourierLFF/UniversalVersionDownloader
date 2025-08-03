import requests
import xml.etree.ElementTree as ET
import os


def neoforge_download(versions):
    print("Downloading NeoForge Maven Data")
    maven_url = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
    versions_list = []

    try:
        response = requests.get(maven_url, stream=True)
        response.raise_for_status()

        maven_xml = response.text

        print("NeoForge Maven Data Downloaded Successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading NeoForge Maven Data: {e}")

    root = ET.fromstring(maven_xml)

    for versionMeta in root.findall(".//versions"):
        for metaVersions in versionMeta:
            versions_list.append(metaVersions.text)

    for version in versions:
        split_version = version.split('.')
        version_name_starter = f"{split_version[1]}.{split_version[2]}"

        good_version_list = []
        for neo_version in versions_list:
            if neo_version.startswith(version_name_starter):
                good_version_list.append(neo_version)

        version_download_url = f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{good_version_list[-1]}/neoforge-{good_version_list[-1]}-installer.jar"
        output_dir = os.path.join("versions/neoforge", version)
        output_file = os.path.join(output_dir, f"{version}.jar")
        os.makedirs(output_dir, exist_ok=True)

        try:
            response = requests.get(version_download_url, stream=True)
            response.raise_for_status()

            print("Downloading NeoForge " + version + " Installer file")
            with open(output_file, "wb") as file:
                for chunk in response.iter_content(8192):
                    file.write(chunk)
            print("Version downloaded successfully to " + output_dir)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading version: {e}")
            continue


