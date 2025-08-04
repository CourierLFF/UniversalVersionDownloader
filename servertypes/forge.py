import requests


def forge_download(versions):
    for version in versions:
        print("Downloading Forge Files HTML")
        forge_files_url = f"https://files.minecraftforge.net/net/minecraftforge/forge/index_{version}.html"
        forge_files_html = ""

        try:
            response = requests.get(forge_files_url)
            response.raise_for_status()

            forge_files_html = response.text

            print("Forge Files HTML Downloaded Successfully")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading Forge Files HTML, invalid version: {e}")
            continue


        print(forge_files_html)

