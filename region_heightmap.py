#!/usr/bin/env python3
import argparse
import pathlib
import json
import sys
from PIL import Image

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
parser.add_argument("--output_dir", default="./data/maps")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-q", "--quiet", action="store_true")
parser.add_argument("--force", action="store_true")
args = parser.parse_args()

class Heightmap:
    def __init__(self, region_x, region_z, chunk_x, chunk_z, data):
        self.region_x = region_x
        self.region_z = region_z
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.data = data

    def get(self, x, y):
        rx = x + (self.chunk_x * 16)
        rz = z + (self.chunk_z * 16)
        return self.data[x + (y*16)], rx, rz

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
json_dir /= "chunk_data"

output_dir = pathlib.Path(args.output_dir).expanduser().resolve()
output_dir /= save_name
output_dir /= "heightmap"

if args.regions is None:
    regions = (x for x in sorted(json_dir.iterdir()) if x.stem.startswith("r"))
else:
    regions = (json_dir / r for r in args.regions)

if args.chunks is None:
    chunks = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunks = args.chunks

for region in regions:
    region_name = region.name
    output_path = output_dir / f"{region_name}.png"
    if output_path.exists() and not args.force:
        if args.verbose:
            print(f"Skipping region {region_name}: already generated")
        continue
    else:
        if not args.quiet:
            print(f"Parsing region {region_name}")

    _, region_x, region_z = region_name.split(".")

    heightmaps = []
    for c in chunks:
        json_path = json_dir / region_name / f"c.{c}.json"
        if not json_path.exists():
            if args.verbose:
                print(f"Skipping chunk {c}: file not found {json_path}")
            continue

        with open(json_path, "r") as f:
            data = json.load(f)

        j = data["Level"]["Heightmaps"]

        try:
            heightmap_ocean_floor_data = j["OCEAN_FLOOR"]
        except KeyError:
            continue

        heightmap = []
        for i, long in enumerate(heightmap_ocean_floor_data):
            vals = util.unpack_heightmap(long)
            if i == len(heightmap_ocean_floor_data) - 1:
                heightmap.extend(vals[:4])
            else:
                heightmap.extend(vals)

        chunk_x, chunk_z = (int(x) for x in c.split("."))
        h = Heightmap(region_x, region_z, chunk_x, chunk_z, heightmap)
        heightmaps.append(h)


    image = Image.new("L", (512, 512))
    data = image.load()
    for heightmap in heightmaps:
        for z in range(16):
            for x in range(16):
                height, rx, rz = heightmap.get(x, z)
                data[rx, rz] = height

    util.write(output_path, "")
    image.save(output_path)
