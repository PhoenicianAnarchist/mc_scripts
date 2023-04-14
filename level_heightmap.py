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

output_dir = pathlib.Path(args.output_dir).expanduser().resolve()
output_dir /= save_name

sub_dir = json_dir / "chunk_data"
all_regions = [x for x in sorted(sub_dir.iterdir()) if x.stem.startswith("r")]
if args.regions is None:
    regions = all_regions
else:
    regions = [json_dir / "chunk_data" / r for r in args.regions]

if args.chunks is None:
    chunks = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunks = args.chunks

generate_new_image = True
output_path = output_dir / f"{save_name}.png"
if output_path.exists():
    if not args.force:
        if args.verbose:
            print(f"Skipping map for {save_name}: already generated")
        sys.exit()
    else:
        generate_new_image = False
        image = Image.open(output_path)

min_x = min_z = max_x = max_z = 0
for region in all_regions:
    region_x, region_z = [int(x) for x in region.name.split(".")[1:]]

    if region_x > max_x:
        max_x = region_x
    elif region_x < min_x:
        min_x = region_x

    if region_z > max_z:
        max_z = region_z
    elif region_z < min_z:
        min_z = region_z

diff_x = max_x - min_x
diff_z = max_z - min_z

img_w = (diff_x + 1) * 512
img_h = (diff_z + 1) * 512

if generate_new_image:
    image = Image.new("L", (img_w, img_h))
else:
    w, h = image.size
    if (w != img_w) or (h != img_h):
        print(f"Error: mis-matched image size! {w} {h} vs {img_w} {img_h}")
        sys.exit(1)


image_data = image.load()

for region in regions:
    region_name = region.name

    if not args.quiet:
        print(f"Parsing region {region_name}")

    region_x, region_z = [int(x) for x in region_name.split(".")[1:]]

    heightmaps = []
    for c in chunks:
        json_path = json_dir / "chunk_data" / region_name / f"c.{c}.json"
        if not json_path.exists():
            if args.verbose:
                print(f"Skipping chunk {c}: file not found {json_path}")
            continue

        with open(json_path, "r") as f:
            data = json.load(f)

        j = data["Level"]["Heightmaps"]

        try:
            heightmap_ocean_floor = j["OCEAN_FLOOR"]
        except KeyError:
            continue

        ocean_floor = []
        for i, long in enumerate(heightmap_ocean_floor):
            vals = util.unpack_heightmap(long)
            if i == len(heightmap_ocean_floor) - 1:
                ocean_floor.extend(vals[:4])
            else:
                ocean_floor.extend(vals)

        chunk_x, chunk_z = (int(x) for x in c.split("."))
        h = Heightmap(region_x, region_z, chunk_x, chunk_z, ocean_floor)
        heightmaps.append(h)

    for heightmap in heightmaps:
        for z in range(16):
            for x in range(16):
                height, rx, rz = heightmap.get(x, z)
                px = ((region_x + min_x) * 512) + rx
                pz = ((region_z + min_z) * 512) + rz
                image_data[px, pz] = height

util.write(output_path, "")
image.save(output_path)
