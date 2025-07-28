import requests
import json
import os

def vanillaDownload(version):
    print("Downloading Vanilla " + version)
    manifestUrl = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    manifestJSON = ""

    try:
        response = requests.get(manifestUrl)
        response.raise_for_status()

        manifestJSON = response.text

        print("Manifest JSON saved successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error saving manifest: {e}")

    versionUrl = ""
    versionJSON = ""

    manifestObject = json.loads(manifestJSON)
    for manifestVersion in manifestObject["versions"]:
        if manifestVersion["id"] == version:
            print("Downloading " + manifestVersion["url"])
            versionUrl = manifestVersion["url"]

    try:
        response = requests.get(versionUrl)
        response.raise_for_status()

        versionJSON = response.text

        print("Version JSON saved successfully")
    except requests.exceptions.RequestException as e:
        print(f"Error saving version: {e}")

    versionObject = json.loads(versionJSON)

    versionDownloadURL = versionObject["downloads"]["server"]["url"]
    output_dir = os.path.join("versions", version)
    output_file = os.path.join(output_dir, f"{version}.jar")
    os.makedirs(output_dir, exist_ok=True)

    try:
        response = requests.get(versionDownloadURL, stream=True)
        response.raise_for_status()

        print("Downloading Vanilla " + version + " JAR file")
        with open(output_file, "wb") as file:
            for chunk in response.iter_content(8192):
                file.write(chunk)
        print("Version downloaded successfully to " + output_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error downloading version: {e}")



