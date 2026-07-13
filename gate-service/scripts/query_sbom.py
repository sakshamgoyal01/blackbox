import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument(
    "package",
    help="Package name to search for",
)

args = parser.parse_args()

root = Path("sbom")

found = False

for sbom in root.glob("*.cdx.json"):

    with open(sbom) as f:
        data = json.load(f)

    for component in data.get("components", []):

        if component.get("name") == args.package:

            print("=" * 60)
            print("SBOM :", sbom.name)
            print("Package :", component["name"])
            print("Version :", component.get("version"))
            print("=" * 60)

            found = True

if not found:
    print("Package not found.")