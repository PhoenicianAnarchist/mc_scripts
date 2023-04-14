#!/usr/bin/env python3
import argparse
import pathlib
import json
import sys

from common import buffer
from common import chunk
from common import poi
from common import util

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config.json")
parser.add_argument("--name", default=None)
parser.add_argument("--regions", nargs="*")
parser.add_argument("--chunks", nargs="*")
parser.add_argument("--json_dir", default="./data/extracted")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("--force", action="store_true")
args = parser.parse_args()

try:
    with open(args.config, "r") as f:
        config = json.load(f)
except:
    print(f"Error: Config file not found `{args.config}`")
    sys.exit(1)

if args.name is None:
    save_name = config["save_name"]
else:
    save_name = args.name

json_dir = pathlib.Path(args.json_dir).expanduser().resolve()
json_dir /= save_name

if args.regions is None:
    sub_dir = json_dir / "chunk_data"
    regions = (x for x in sorted(sub_dir.iterdir()) if x.stem.startswith("r"))
else:
    regions = (json_dir / r for r in args.regions)

if args.chunks is None:
    chunks = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunks = args.chunks

structure_data = []
for region in regions:
    region_name = region.name
    if not args.quiet:
        print(f"Parsing region {region_name}")

    for c in chunks:
        path = json_dir / "chunk_data" / region_name / f"c.{c}.json"
        if not path.exists():
            if args.verbose:
                print(f"Skipping chunk {c}: file not found {path}")
            continue

        with open(path, "r") as f:
            data = json.load(f)

        j = data["Level"]

        references = j["Structures"]["References"]
        for name, longs in references.items():
            if longs == []:
                continue

            for long in longs:
                x, z = util.xz_from_64(long)
                s = poi.POISmall(name, x * 16, 0, z * 16)
                if s not in structure_data:
                    structure_data.append(s)

        starts = j["Structures"]["Starts"]
        for name, data in starts.items():
            if data["id"] == "INVALID":
                continue

            x = data["ChunkX"]
            z = data["ChunkZ"]

            s = poi.POISmall(name, x * 16, 0, z * 16)
            if s not in structure_data:
                structure_data.append(s)

path = json_dir / "structures.json"
util.write(path, json.dumps(structure_data, indent=2, sort_keys=True, cls=poi.POIJSONEncoder))
