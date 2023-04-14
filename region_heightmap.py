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
parser.add_argument("--path", default=None)
parser.add_argument("--regions", nargs="*")
parser.add_argument("--chunks", nargs="*")
parser.add_argument("--output_dir", default="./data/maps")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()

class Heightmap:
    def __init__(self, region_x, region_z, chunk_x, chunk_z, ocean, surface):
        self.region_x = region_x
        self.region_z = region_z
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.ocean_floor = ocean_floor
        self.surface = surface

    def get(self, x, y):
        rx = x + (self.chunk_x * 16)
        rz = z + (self.chunk_z * 16)
        return self.ocean_floor[x + (y*16)], rx, rz

try:
    with open(args.config, "r") as f:
        config = json.load(f)
except:
    print(f"Error: Config file not found `{args.config}`")
    sys.exit(1)

if args.path is None:
    save_path = config["path"]
else:
    save_path = args.path

save_path = pathlib.Path(save_path).expanduser().resolve()
save_name = save_path.name
region_directory = save_path / "region"

output_dir = pathlib.Path(args.output_dir).expanduser().resolve()
output_dir /= save_name
output_dir /= "heightmap"

if args.regions is None:
    region_files = sorted(region_directory.iterdir())
else:
    region_files = [region_directory / r for r in args.regions]

if args.chunks is None:
    chunks = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunks = args.chunks

structure_data = []
for region_file in region_files:
    region_name = region_file.stem
    _, region_x, region_z = region_name.split('.')

    if not args.quiet:
        print(f"Parsing region {region_name}")

    data = util.read_raw(region_file)
    buf = buffer.Buffer(data)

    index_table = buf.read(4096)
    timestamp_table = buf.read(4096)

    index_buffer = buffer.Buffer(index_table)
    timestamp_buffer = buffer.Buffer(timestamp_table)

    heightmaps = []
    for c in chunks:
        if args.verbose:
            print(f"Parsing chunk {c}")
        chunk_x, chunk_z = [int(x) for x in c.split(".")]
        chunk_data = chunk.get_chunk(chunk_x, chunk_z, buf)

        if chunk_data is None:
            continue

        nbt = buffer.NBTBuffer(chunk_data.data)
        j = nbt.root.to_json()[""]["Level"]

        x_pos = j["xPos"]
        z_pos = j["zPos"]

        try:
            heightmap_ocean_floor = j["Heightmaps"]["OCEAN_FLOOR"]
        except KeyError:
            continue

        ocean_floor = []
        for i, long in enumerate(heightmap_ocean_floor):
            vals = util.unpack_heightmap(long)
            if i == len(heightmap_ocean_floor) - 1:
                ocean_floor.extend(vals[:4])
            else:
                ocean_floor.extend(vals)

        try:
            heightmap_world_surface = j["Heightmaps"]["WORLD_SURFACE"]
        except KeyError:
            continue

        surface = []
        for i, long in enumerate(heightmap_world_surface):
            vals = util.unpack_heightmap(long)
            if i == len(heightmap_world_surface) - 1:
                surface.extend(vals[:4])
            else:
                surface.extend(vals)

        h = Heightmap(region_x, region_z, chunk_x, chunk_z, ocean_floor, surface)
        heightmaps.append(h)


    image = Image.new("L", (512, 512))
    data = image.load()
    for heightmap in heightmaps:
        for z in range(16):
            for x in range(16):
                height, rx, rz = heightmap.get(x, z)
                data[rx, rz] = height

    path = output_dir / f"{region_name}.png"
    util.write(path, "")
    image.save(path)
