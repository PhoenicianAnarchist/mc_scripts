#!/usr/bin/env python3
import argparse
import pathlib
import json
import sys
import gzip
import zlib

from common import buffer
from common import tag
from common import util

# Example path: ~/.local/share/multimc/instances/<instance name>/.minecraft/saves/<save name>
parser = argparse.ArgumentParser()

parser.add_argument("filepath")
parser.add_argument("--output_dir", default="./data/mca")
parser.add_argument("-v", "--verbose", action="store_true")

args = parser.parse_args()

class Chunk:
    def __init__(self, x, z, timestamp, compression_type, payload):
        self.x = x
        self.z = z
        self.timestamp = timestamp
        self.data = None

        if compression_type == 1:
            self.data = gzip.decompress(payload)
        elif compression_type == 2:
            self.data = zlib.decompress(payload)
        elif compression_type == 3:
            self.data = payload
        else:
            print(f"{x} {z} {timestamp}")
            raise ValueError(f"Invalid compression type {compression_type}")

class POI:
    def __init__(self, region_name, name, cx, cz, x, y, z):
        _, rx, rz = region_name.split(".")

        self.name = name
        self.region_x = int(rx)
        self.region_z = int(rz)
        self.chunk_x = cx
        self.chunk_z = cz
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        s = "X{:>6}, Y{:>4}, Z{:>6} ({:<10} : {:<10}) {}"
        r = f"r.{self.region_x}.{self.region_z}"
        c = f"c.{self.chunk_x}.{self.chunk_z}"

        return s.format(self.x, self.y, self.z, r, c, self.name)

    def to_json(self):
        return {
            "name": self.name,
            "region_x": self.region_x,
            "region_z": self.region_z,
            "chunk_x": self.chunk_x,
            "chunk_z": self.chunk_z,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

class POIJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json()

def get_chunk(x, z, buf):
    index = ((x & 31) + (z & 31) * 32)
    index_offset = index * 4

    buf.seek(index_offset)
    sector_offset = int.from_bytes(buf.read(3), "big")
    sector_count = int.from_bytes(buf.read(1), "big")

    if sector_offset == sector_count == 0:
        # chunk not yet populated
        return None

    buf.seek(index_offset + 4096)
    timestamp = int.from_bytes(buf.read(4), "big")

    offset, count = to_index(sector_offset, sector_count)
    buf.seek(offset)
    data_length = int.from_bytes(buf.read(4), "big")
    compression_type = int.from_bytes(buf.read(1), "big")
    payload = buf.read(data_length - 1)

    return Chunk(x, z, timestamp, compression_type, payload)

def to_index(offset, count):
    o = (offset * 4096)
    c = (count * 4096)
    return o, c

filepath = pathlib.Path(args.filepath).resolve()
save_name = filepath.name
filepath /= "region"

output_dir = pathlib.Path(args.output_dir).resolve()
output_dir /= save_name

poi_data = {}

for region_filepath in filepath.iterdir():
    region_name = region_filepath.stem
    _, region_x, region_z = region_name.split('.')
    print(f"Parsing region {region_name}")

    poi_data[region_name] = []

    bin_dir = output_dir / f"bin/{region_x}/{region_z}"
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
            chunk = get_chunk(x, z, buf)

            if chunk is None:
                if args.verbose:
                    print("-> not populated")
                continue

            nbt = buffer.NBTBuffer(chunk.data)
            j = nbt.root.to_json()
            xpos = j["Level"]["xPos"]
            zpos = j["Level"]["zPos"]

            if args.verbose:
                print(f"@ {xpos} {zpos}")


            min_structures = {}
            structures = j["Level"]["Structures"]["Starts"]
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
                p = POI(
                    region_name, k,
                    x, z,
                    child_0["x"], child_0["y"], child_0["z"]
                )
                print(p)
                poi_data[region_name].append(p)

            min_json = {
                "Chunk": {
                    "x": xpos,
                    "z": zpos,
                    # "TileEntities": j["Level"]["TileEntities"],
                    # "Entities": j["Level"]["Entities"],
                    "Structures": min_structures
                }
            }

            if len(min_structures) >= 1:
                json_path = json_dir / f"c.{x}.{z}.json"
                util.write(json_path, json.dumps(min_json, indent=2))

util.write(output_dir / "poi.json", json.dumps(poi_data, indent=2, cls=POIJSONEncoder))
