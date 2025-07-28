import argparse

parser = argparse.ArgumentParser(description='Universal Version Downloader')

parser.add_argument('modloader', type=str, help='Selected Modloader')
parser.add_argument('version', type=str, help='Selected Version')

args = parser.parse_args()
print("You selected " + args.modloader + " on " + args.version)