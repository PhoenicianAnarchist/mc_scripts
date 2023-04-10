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
filepath /= "region"

output_dir = pathlib.Path(args.output_dir).resolve()
output_dir /= save_name
output_dir /= "region"

structure_data = []

for region_filepath in filepath.iterdir():
    region_name = region_filepath.stem
    _, region_x, region_z = region_name.split('.')
    print(f"Parsing region {region_name}")

    json_dir = output_dir / f"json/{region_x}/{region_z}"

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

            nbt = buffer.NBTBuffer(chunk_data.data)
            j = nbt.root.to_json()[""]["Level"]
            xpos = j["xPos"]
            zpos = j["zPos"]

            if args.verbose:
                print(f"@ {xpos} {zpos}")

            min_structures = {}
            structures = j["Structures"]["Starts"]
            for k, v in structures.items():
                if v["id"] == "INVALID":
                    continue

                s = {
                    "Children": []
                }
                for child in v["Children"]:
                    c = {
                        "id": child["id"],
                        "x": child.get("PosX", x * 16),
                        "y": child.get("PosY", 0),
                        "z": child.get("PosZ", z * 16)
                    }

                    s["Children"].append(c)

                min_structures[k] = s
                child_0 = s["Children"][0]
                p = poi.POI(
                    region_name, k,
                    x, z,
                    child_0["x"], child_0["y"], child_0["z"]
                )
                print(p)
                structure_data.append(p)

            min_json = {
                "Chunk": {
                    "x": xpos,
                    "z": zpos,
                    # "TileEntities": j["TileEntities"],
                    # "Entities": j["Entities"],
                    "Structures": min_structures
                }
            }

            if len(min_structures) >= 1:
                json_path = json_dir / f"c.{x}.{z}.json"
                util.write(json_path, json.dumps(min_json, indent=2))

util.write(output_dir / "structures.json", json.dumps(structure_data, indent=2, cls=poi.POIJSONEncoder))
