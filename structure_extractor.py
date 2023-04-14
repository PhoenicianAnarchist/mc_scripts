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
parser.add_argument("--path", default=None)
parser.add_argument("--regions", nargs="*")
parser.add_argument("--chunks", nargs="*")
parser.add_argument("--output_dir", default="./data/mca")
parser.add_argument("-v", "--verbose", action="store_true")
parser.add_argument("-q", "--quiet", action="store_true")
args = parser.parse_args()

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
    if not args.quiet:
        print(f"Parsing region {region_name}")

    data = util.read_raw(region_file)
    buf = buffer.Buffer(data)

    index_table = buf.read(4096)
    timestamp_table = buf.read(4096)

    index_buffer = buffer.Buffer(index_table)
    timestamp_buffer = buffer.Buffer(timestamp_table)

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

path = output_dir / f"structures.json"
util.write(path, json.dumps(structure_data, indent=2, sort_keys=True, cls=poi.POIJSONEncoder))
