import argparse

from modloaders.fabric import fabric_download
from modloaders.paper import paper_download
from modloaders.vanilla import vanilla_download

def main():
    parser = argparse.ArgumentParser(description='Universal Version Downloader')

    parser.add_argument('modloader', type=str, help='Selected Modloader / Server Software (Vanilla, Fabric)')
    parser.add_argument('versions', nargs='+', help='Selected Version or Versions')

    args = parser.parse_args()
    print("You selected " + args.modloader + " on " + str(args.versions))

    selected_modloader = args.modloader.lower()

    match selected_modloader:
        case "vanilla":
            vanilla_download(args.versions)
        case "fabric":
            fabric_download(args.versions)
        case "paper":
            paper_download(args.versions)
        case _:
            print("Invalid Modloader / Server Software")

main()