import requests
import xml.etree.ElementTree as ET
import os
import subprocess
import shutil


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

        if not good_version_list:
            print(f"Version {version} not found in NeoForge Maven Data")
            continue

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
            print("Version installer downloaded successfully to " + output_dir)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading version installer: {e}")
            continue

        if not os.path.isdir(output_dir):
            print(f"Error: Directory {output_dir} does not exist")
            continue
        else:
            try:
                print(f"Installing NeoForge {version} server... (May take a few moments)")
                result = subprocess.run(["java", "-jar", f"{version}.jar", "--installServer"], cwd=output_dir, capture_output=True, text=True, check=True)
                print(f"NeoForge {version} server installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {e}")
                print(f"Stderr: {e.stderr}")

        print("Cleaning NeoForge installed files")
        for item_name in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item_name)
            if os.path.isfile(item_path):
                os.remove(item_path)
        print("Cleaned NeoForge installed files successfully")

        try:
            shutil.copy("serverstarterjar/server.jar", output_dir)
            print(f"Finished copying server starter jar to {output_dir}")
        except FileNotFoundError:
            print(f"Server starter jar not found")
        except Exception as e:
            print(f"An error occurred: {e}")

        print("Creating EULA file")
        eula_dir = os.path.join(output_dir, "eula.txt")
        with open(eula_dir, "w") as file:
            file.write("eula=true")
        print("Created EULA file successfully")

        print("Zipping files")
        shutil.make_archive(f"{version}", "zip", output_dir)
        shutil.move(f"{version}.zip", output_dir)
        print("Finished zipping files")



