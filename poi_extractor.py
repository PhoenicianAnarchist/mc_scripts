#!/usr/bin/env python3
import argparse
import pathlib
import json

from common import buffer
from common import chunk
from common import poi
from common import util

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config.json")
parser.add_argument("--path", default=None)
parser.add_argument("--save_name", default=None)
parser.add_argument("--regions", nargs="*")
parser.add_argument("--chunks", nargs="*")
parser.add_argument("--output_dir", default="./data/extracted")
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

if args.path is None:
    save_name = config["save_name"]
    save_path = pathlib.Path(config["path"].format(save_name)).expanduser().resolve()
else:
    save_path = pathlib.Path(args.path)
    save_name = save_path.name

region_directory = save_path / "poi"

output_dir = pathlib.Path(args.output_dir).expanduser().resolve()
output_dir /= save_name

if args.regions is None:
    region_files = sorted(region_directory.iterdir())
else:
    region_files = (region_directory / r for r in args.regions)

if args.chunks is None:
    chunks = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunks = args.chunks

poi_data = []

for region_file in region_files:
    region_name = region_file.stem
    if not args.quiet:
        print(f"Parsing region {region_name}")

    data = util.read_raw(region_file)
    buf = buffer.Buffer(data)

    for c in chunks:
        chunk_x, chunk_z = [int(x) for x in c.split(".")]
        chunk_data = chunk.get_chunk(chunk_x, chunk_z, buf)
        if chunk_data is None:
            if args.verbose:
                print(f"Skipping chunk {c}: no poi data available")
            continue

        nbt = buffer.NBTBuffer(chunk_data.data)
        j = nbt.root.to_json()[""]["Sections"]

        print(j)

        for section, data in j.items():
            records = data["Records"]

            for record in records:
                name = record["type"]
                x_pos, y_pos, z_pos = record["pos"]

                p = poi.POISmall(
                    name,
                    x_pos, y_pos, z_pos
                )
                print(p)
                if p not in poi_data:
                    poi_data.append(p)

path = output_dir / "poi.json"
util.write(path, json.dumps(poi_data, indent=2, cls=poi.POIJSONEncoder))
