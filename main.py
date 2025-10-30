import requests
import json
import os

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

def main():
    selected_modloader = "vanilla"
    version = "1.21.10"

    match selected_modloader:
        case "vanilla":
            vanilla_download(version)
        # case "fabric":
        #     fabric_download(version)
        # case "paper":
        #     paper_download(version)
        # case "purpur":
        #     purpur_download(version)
        # case "neoforge":
        #     neoforge_download(version)
        # case "forge":
        #     forge_download(version)
        case _:
            print("Invalid Modloader / Server Software")

main()