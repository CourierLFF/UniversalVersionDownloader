# UniversalVersionDownloader
A script for downloading server versions from multiple Minecraft server types

## Supported Server Types
- Vanilla (Including Snapshots)
- Forge
- Fabric
- NeoForge
- Paper
- PurPur

## Installation

### Prerequisites
- Java 21
- Python 3.13 (Most versions of Python 3 should work, but this is the version I tested)

Dependencies install

`pip install -r requirements.txt`

## Usage

The syntax for this script looks like this. Ensure that each version is seperated by a space. Only one modloader supported for each command.

`python .\main [modloader] [versions]`

When finished, the script will make a versions directory in the script's directory and put the downloaded and installed files into there. It will rename the .jar files for Vanilla, Fabric, PurPur and Paper into [Minecraft version].jar. For NeoForge and Forge, it will archive neccesary files into a zip file and rename it to [Minecraft version].zip for Forge and [NeoForge version].zip for NeoForge.

### Examples
Vanilla 1.21.8

`python .\main.py vanilla 1.21.8`

Fabric 1.20.1 and 1.21.1

`python .\main.py fabric 1.20.1 1.21.1`

PurPur 1.21.5, 1.17, and 1.18.2

`python .\main.py purpur 1.21.5 1.17 1.18.2`


## Known Limitations
At the moment, Forge does not have any consistent way to get download links for their versions. As a result I have to scrape their webpage for download links.
This works fine for most versions however some versions have slightly different URLs. The most popular version I could find with a different URL is 1.7.10, so for the time being this version's URL is hardcoded into the script.

I have only tested this script on Windows, support for macOS and Linux will not be provided.

