import requests
import json
import os
import shutil
import xml.etree.ElementTree as ET
import subprocess
from bs4 import BeautifulSoup
import re

def vanilla_download(version):
    print("Downloading Vanilla " + version)
    # Vanilla has a json file that contains all version information including server jar download links
    manifest_url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifest_json = ""

    try:
        response = requests.get(manifest_url)
        response.raise_for_status()

        manifest_json = response.text

        print("Manifest JSON saved successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error saving manifest: {e}")
        return None

    version_url = ""
    version_json = ""

    # Load the json file as an object and find the selected Minecraft version in the json, then get the URL to that specific version's json file
    manifest_object = json.loads(manifest_json)
    for manifest_version in manifest_object["versions"]:
        if manifest_version["id"] == version:
            print("Downloading " + manifest_version["url"])
            version_url = manifest_version["url"]

    try:
        response = requests.get(version_url)
        response.raise_for_status()

        version_json = response.text

        print("Version JSON saved successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error saving version: {e}")
        return None

    # Load the version json into an object and then get the server download URL from it
    version_object = json.loads(version_json)

    version_download_url = version_object["downloads"]["server"]["url"]
    output_dir = "/"
    output_file = os.path.join(output_dir, "server.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(version_download_url, stream=True)
        response.raise_for_status()

        print("Downloading Vanilla " + version + " JAR file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version: {e}")
        return None
    
    # Copy server jar to also have prod ready format
    try:
        shutil.copyfile(output_file, f"/{version}.jar")
    except FileNotFoundError as e:
        print(f"Error copying file: {e}")
        return None

def fabric_download(version):
    fabric_loader_version = ""
    # Get all fabric loader versions
    response = requests.get("https://meta.fabricmc.net/v2/versions/loader")
    data = response.json()

    # Select newest fabric loader version
    if data:
        fabric_loader_version = data[0]["version"]
        print(f"Latest Fabric Loader version: {fabric_loader_version}")
    else:
        print("Could not retrieve Fabric Loader versions.")
        return None

    print("Downloading Fabric " + version)

    # Fabric offers this URL on their server download page. 1.1.0 represents the installer version. This installer version may need to be changed in the future for compatibility, but as of now it updates infrequently enough and doesn't seem to have any compatibility issues.
    version_download_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{fabric_loader_version}/1.1.0/server/jar"
    output_dir = "/"
    output_file = os.path.join(output_dir, "server.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(version_download_url, stream=True)
        response.raise_for_status()

        print("Downloading Fabric " + version + " JAR file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version: {e}")
        return None
    
    # Copy server jar to also have prod ready format
    try:
        shutil.copyfile(output_file, f"/{version}.jar")
    except FileNotFoundError as e:
        print(f"Error copying file: {e}")
        return None

def paper_download(version):
    print("Downloading Paper " + version)
    paper_builds_url = f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds"
    paper_builds_json = ""

    try:
        response = requests.get(paper_builds_url)
        response.raise_for_status()

        paper_builds_json = response.json()

        print("Paper builds JSON saved successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error saving paper builds: {e}")
        return None

    # Parse the builds json and get the latest paper build for the selected version
    version_download_url = paper_builds_json[0]["downloads"]["server:default"]["url"]
    output_dir = "/"
    output_file = os.path.join(output_dir, "server.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(version_download_url, stream=True)
        response.raise_for_status()

        print("Downloading Paper " + version + " JAR file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version: {e}")
        return None
    
    # Copy server jar to also have prod ready format
    try:
        shutil.copyfile(output_file, f"/{version}.jar")
    except FileNotFoundError as e:
        print(f"Error copying file: {e}")
        return None

def purpur_download(version):
    print("Downloading PurPur " + version)

    version_download_url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
    output_dir = "/"
    output_file = os.path.join(output_dir, "server.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(version_download_url, stream=True)
        response.raise_for_status()

        print("Downloading PurPur " + version + " JAR file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version: {e}")
        return None
    
    # Copy server jar to also have prod ready format
    try:
        shutil.copyfile(output_file, f"/{version}.jar")
    except FileNotFoundError as e:
        print(f"Error copying file: {e}")
        return None

def neoforge_download(version):
    print("Downloading NeoForge Maven Data")
    # NeoForge has a helpful XML document that contains the names of all the NeoForge versions.
    maven_url = "https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml"
    versions_list = []

    try:
        response = requests.get(maven_url, stream=True)
        response.raise_for_status()

        maven_xml = response.text

        print("NeoForge Maven Data Downloaded Successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading NeoForge Maven Data: {e}")
        return None

    root = ET.fromstring(maven_xml)

    # Parse the XML document to find all versions and then add them to a list containing all versions correlating to the selected Minecraft version
    for versionMeta in root.findall(".//versions"):
        for metaVersions in versionMeta:
            versions_list.append(metaVersions.text)

    split_version = version.split('.')
    # NeoForge versions have a consistent naming scheme. They begin with the minor version in Minecraft, then have the patch number, then the NeoForge patch number.
    # Some examples of this would be all Minecraft 1.21.1 NeoForge versions starting with 21.1. and all 1.20.4 versions starting with 20.4.
    # This consistent naming scheme is used to find all NeoForge versions compatible with our selected Minecraft version, and then select the latest one.
    version_name_starter = f"{split_version[1]}.{split_version[2]}"

    good_version_list = []
    for neo_version in versions_list:
        if neo_version.startswith(version_name_starter):
            good_version_list.append(neo_version)

    if not good_version_list:
        print(f"Version {version} not found in NeoForge Maven Data")
        return None

    version_download_url = f"https://maven.neoforged.net/releases/net/neoforged/neoforge/{good_version_list[-1]}/neoforge-{good_version_list[-1]}-installer.jar"
    output_dir = "/"
    output_file = os.path.join(output_dir, "installer.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(version_download_url, stream=True)
        response.raise_for_status()

        print("Downloading NeoForge " + version + " Installer file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version installer downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version installer: {e}")
        return None

    if not os.path.isdir(output_dir):
        print(f"Error: Directory {output_dir} does not exist")
        return None
    else:
        try:
            print(f"Installing NeoForge {version} server... (May take a few moments)")
            result = subprocess.run(["java", "-jar", "/installer.jar", "--installServer"], cwd=output_dir, capture_output=True, text=True, check=True)
            print(f"NeoForge {version} server installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Stderr: {e.stderr}")
            return None

    print("Cleaning NeoForge installed files")
    for item_name in os.listdir(output_dir):
        item_path = os.path.join(output_dir, item_name)
        if os.path.isfile(item_path):
            os.remove(item_path)
    print("Cleaned NeoForge installed files successfully")

    try:
        response = requests.get("https://github.com/neoforged/ServerStarterJar/releases/download/0.1.34/server.jar", stream=True)
        response.raise_for_status()

        with open("/server.jar", "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print(f"Finished downloading server starter jar")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading version installer: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    print("Creating EULA file")
    eula_dir = os.path.join(output_dir, "eula.txt")
    with open(eula_dir, "w") as file:
        file.write("eula=true")
    print("Created EULA file successfully")

    print("Zipping files")
    shutil.make_archive(f"{good_version_list[-1]}", "zip", output_dir)
    shutil.move(f"{good_version_list[-1]}.zip", output_dir)
    print("Finished zipping files")

def forge_download(version):
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
        return None

    # Parsing the HTML to find the meta description tag in the head. This tag contains the lastest version of the selected Minecraft version.
    soup = BeautifulSoup(forge_files_html, "html.parser")

    description_tag = soup.find("meta", property="og:description")

    match = re.search(r'Latest:\s*([\d.]+)', description_tag.get("content"))
    if match:
        latest_forge_version = match.group(1)
        print(f"Latest Version: {latest_forge_version}")
    else:
        print(f"Cannot find latest forge version for {version}")
        return None

    version_download_url = f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{latest_forge_version}/forge-{version}-{latest_forge_version}-installer.jar"
    # For some reason random versions use a different URL scheme, 1.7.10 seems to be the most popular version that uses a different URL scheme, so I'll just hardcode it in for now until I come up with a better solution.
    output_dir = "/"
    output_file = os.path.join(output_dir, "installer.jar")
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
        return None

    if not os.path.isdir(output_dir):
        print(f"Error: Directory {output_dir} does not exist")
        return None
    else:
        try:
            print(f"Installing Forge {version} server... (May take a few moments)")
            result = subprocess.run(["java", "-jar", "installer.jar", "--installServer"], cwd=output_dir, capture_output=True, text=True, check=True)
            print(f"Forge {version} server installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Stderr: {e.stderr}")
            return None

        print("Cleaning Forge installed files")
        for item_name in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item_name)
            if os.path.isfile(item_path) and not "shim" in item_name:
                os.remove(item_path)
        print("Cleaned Forge installed files successfully")

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

def main():
    selected_modloader = os.environ.get("SERVER_TYPE")
    version = os.environ.get("MINECRAFT_VERSION")

    if selected_modloader == "vanilla":
        vanilla_download(version)
    elif selected_modloader == "fabric":
        fabric_download(version)
    elif selected_modloader == "paper":
        paper_download(version)
    elif selected_modloader == "purpur":
        purpur_download(version)
    elif selected_modloader == "neoforge":
        neoforge_download(version)
    elif selected_modloader == "forge":
        forge_download(version)
    else:
        print("Invalid Modloader / Server Software")

main()