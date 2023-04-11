#!/usr/bin/env python3
import argparse
import pathlib
import json

from common import buffer
from common import chunk
from common import poi
from common import util

# Example path: ~/.local/share/multimc/instances/<instance name>/.minecraft/saves/<save name>
parser = argparse.ArgumentParser()

parser.add_argument("filepath")
parser.add_argument("--output_dir", default="./data/mca")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

filepath = pathlib.Path(args.filepath).resolve()
save_name = filepath.name
filepath /= "poi"

output_dir = pathlib.Path(args.output_dir).resolve()
output_dir /= save_name
output_dir /= "poi"

poi_data = []

for region_filepath in filepath.iterdir():
    region_name = region_filepath.stem
    _, region_x, region_z = region_name.split('.')
    print(f"Parsing region {region_name}")

    data = util.read_raw(region_filepath)
    buf = buffer.Buffer(data)

    index_table = buf.read(4096)
    timestamp_table = buf.read(4096)

    index_buffer = buffer.Buffer(index_table)
    timestamp_buffer = buffer.Buffer(timestamp_table)

    for x in range(32):
        for z in range(32):
            if args.verbose:
                print(f"  Parsing chunk {x}, {z} ", end="")

            chunk_data = chunk.get_chunk(x, z, buf)

            if chunk_data is None:
                if args.verbose:
                    print("-> not populated")
                continue

            if args.verbose:
                print()

            nbt = buffer.NBTBuffer(chunk_data.data)
            j = nbt.root.to_json()[""]["Sections"]

            for section, data in j.items():
                records = data["Records"]

                print(f"Section {section}: {len(records)} records")
                for record in records:
                    name = record["type"]
                    x, y, z = record["pos"]

                    p = poi.POI(region_name, name, 0, 0, x, y, z)
                    poi_data.append(p)

                    print(p)

util.write(output_dir / "poi.json", json.dumps(poi_data, indent=2, cls=poi.POIJSONEncoder))
