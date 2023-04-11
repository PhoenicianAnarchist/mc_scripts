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
parser.add_argument("-q", "--quiet", action="store_true")

args = parser.parse_args()

filepath = pathlib.Path(args.filepath).resolve()
save_name = filepath.name
filepath /= "region"

output_dir = pathlib.Path(args.output_dir).resolve()
output_dir /= save_name
output_dir /= "region"

structure_data = []

for region_filepath in sorted(filepath.iterdir()):
    region_name = region_filepath.stem
    _, region_x, region_z = region_name.split('.')
    if not args.quiet:
        print(f"Parsing region {region_name}")

    data = util.read_raw(region_filepath)
    buf = buffer.Buffer(data)

    index_table = buf.read(4096)
    timestamp_table = buf.read(4096)

    index_buffer = buffer.Buffer(index_table)
    timestamp_buffer = buffer.Buffer(timestamp_table)

    for chunk_x in range(32):
        for chunk_z in range(32):
            if args.verbose:
                print(f"  Parsing chunk {chunk_x}, {chunk_z} ", end="")

            chunk_data = chunk.get_chunk(chunk_x, chunk_z, buf)

            if chunk_data is None:
                if args.verbose:
                    print("-> not populated")
                continue

            nbt = buffer.NBTBuffer(chunk_data.data)
            j = nbt.root.to_json()[""]["Level"]
            xpos = j["xPos"]
            zpos = j["zPos"]

            if args.verbose:
                print(f"@ {xpos} {zpos}")

            structures = j["Structures"]["Starts"]

            for k, v in structures.items():
                if v["id"] == "INVALID":
                    continue

                r = {
                    "name": v["id"],
                    "chunk_x": chunk_x,
                    "chunk_z": chunk_z,
                    "children": []
                }

                for child in v["Children"]:
                    p = poi.POISmall(
                        child.get("id", k),
                        child.get("PosX", chunk_x * 16),
                        child.get("PosY", 0),
                        child.get("PosZ", chunk_z * 16)
                    )

                    r["children"].append(p)

                structure_data.append(r)

    util.write(output_dir / f"{region_name}.json", json.dumps(structure_data, indent=2, cls=poi.POIJSONEncoder))
