import argparse

from modloaders.vanilla import vanilla_download

def main():
    parser = argparse.ArgumentParser(description='Universal Version Downloader')

    parser.add_argument('modloader', type=str, help='Selected Modloader')
    parser.add_argument('version', type=str, help='Selected Version')

    args = parser.parse_args()
    print("You selected " + args.modloader + " on " + args.version)

    selected_modloader = args.modloader.lower()

    match selected_modloader:
        case "vanilla":
            vanilla_download(args.version)
        case _:
            print("Invalid Modloader")

main()