import json
import requests
import os

def paper_download(versions):
    for version in versions:
        paper_builds_url = f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds"
        paper_builds_json = ""

        try:
            response = requests.get(paper_builds_url)
            response.raise_for_status()

            paper_builds_json = response.json()

            print("Paper builds JSON saved successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error saving paper builds: {e}")
            continue

        version_download_url = paper_builds_json[0]["downloads"]["server:default"]["url"]
        output_dir = os.path.join("versions/paper", version)
        output_file = os.path.join(output_dir, f"{version}.jar")
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

