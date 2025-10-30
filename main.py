import requests
import json
import os
import shutil

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

def main():
    selected_modloader = "purpur"
    version = "1.21.10"

    match selected_modloader:
        case "vanilla":
            vanilla_download(version)
        case "fabric":
            fabric_download(version)
        case "paper":
            paper_download(version)
        case "purpur":
            purpur_download(version)
        # case "neoforge":
        #     neoforge_download(version)
        # case "forge":
        #     forge_download(version)
        case _:
            print("Invalid Modloader / Server Software")

main()