import requests
import os

def fabric_download(versions):
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

    for version in versions:
        print("Downloading Fabric " + version)

        # Fabric offers this URL on their server download page. 1.0.3 represents the installer version. This installer version may need to be changed in the future for compatibility, but as of now it updates infrequently enough and doesn't seem to have any compatibility issues.
        version_download_url = f"https://meta.fabricmc.net/v2/versions/loader/{version}/{fabric_loader_version}/1.0.3/server/jar"
        output_dir = os.path.join("versions/fabric", version)
        output_file = os.path.join(output_dir, f"{version}.jar")
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
            continue