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
parser.add_argument("--verbose", action="store_true")

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

for region_filepath in filepath.iterdir():
    region_name = region_filepath.stem
    _, region_x, region_z = region_name.split(".")
    print(f"Parsing region {region_name}")

    bin_dir = output_dir / f"bin/r.{region_x}.{region_z}"
    if not bin_dir.is_dir():
        bin_dir.mkdir(parents=True)

    json_dir = output_dir / f"json/r.{region_x}.{region_z}"
    if not json_dir.is_dir():
        json_dir.mkdir(parents=True)

    data = util.read_raw(region_filepath)
    buf = buffer.Buffer(data, bin_dir)

    index_table = buf.read(4096)
    timestamp_table = buf.read(4096)

    index_buffer = buffer.Buffer(index_table, bin_dir)
    timestamp_buffer = buffer.Buffer(timestamp_table, bin_dir)

    for x in range(32):
        for z in range(32):
            if args.verbose:
                print(f"  Parsing chunk {x}, {z} ", end="")
            chunk = get_chunk(x, z, buf)

            if chunk is None:
                if args.verbose:
                    print("-> not populated")
                continue

            nbt = buffer.NBTBuffer(chunk.data, bin_dir)
            j = nbt.root.json()
            xpos = j[""]["Level"]["xPos"]
            zpos = j[""]["Level"]["zPos"]

            if args.verbose:
                print(f"@ {xpos} {zpos}")
            json_path = json_dir / f"c.{xpos}.{zpos}.json"
            with open(json_path, "w") as f:
                json.dump(j, f, indent=2)
