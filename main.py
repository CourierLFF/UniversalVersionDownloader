import argparse

from servertypes.fabric import fabric_download
from servertypes.neoforge import neoforge_download
from servertypes.paper import paper_download
from servertypes.purpur import purpur_download
from servertypes.vanilla import vanilla_download
from servertypes.forge import forge_download

def main():
    parser = argparse.ArgumentParser(description='Universal Version Downloader')

    parser.add_argument('servertype', type=str, help='Selected Server Type (Vanilla, Fabric, Paper, PurPur, NeoForge, Forge)')
    parser.add_argument('versions', nargs='+', help='Selected Version or Versions')

    args = parser.parse_args()
    print("You selected " + args.servertype + " on " + str(args.versions))

    selected_modloader = args.servertype.lower()

    match selected_modloader:
        case "vanilla":
            vanilla_download(args.versions)
        case "fabric":
            fabric_download(args.versions)
        case "paper":
            paper_download(args.versions)
        case "purpur":
            purpur_download(args.versions)
        case "neoforge":
            neoforge_download(args.versions)
        case "forge":
            forge_download(args.versions)
        case _:
            print("Invalid Modloader / Server Software")

main()