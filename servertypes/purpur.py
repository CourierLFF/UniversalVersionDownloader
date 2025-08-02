import os
import requests

def purpur_download(versions):
    for version in versions:
        print("Downloading PurPur " + version)

        version_download_url = f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
        output_dir = os.path.join("versions/purpur", version)
        output_file = os.path.join(output_dir, f"{version}.jar")
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
            continue