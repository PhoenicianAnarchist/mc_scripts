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

## ~/.local/share/multimc/instances/Create- Above and Beyond/.minecraft/saves/March/region
parser = argparse.ArgumentParser()

parser.add_argument("filepath")

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

def get_chunk(x, z, buf):
    index = ((x & 31) + (z & 31) * 32)
    index_offset = index * 4

    buf.seek(index_offset)
    sector_offset = int.from_bytes(buf.read(3), "big")
    sector_count = int.from_bytes(buf.read(1), "big")
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
filename = filepath.stem
suffix = filepath.suffix
_, region_x, region_z = filename.split(".")

zlib_dir = util.new_path(filepath, f"zlib/r.{region_x}.{region_z}", ".zlib", mkdir=True).parent
bin_dir = util.new_path(filepath, f"bin/r.{region_x}.{region_z}", ".bin", mkdir=True).parent
data = util.read_raw(filepath)

buf = buffer.Buffer(data, bin_dir)

index_table = buf.read(4096)
timestamp_table = buf.read(4096)

index_buffer = buffer.Buffer(index_table, bin_dir)
timestamp_buffer = buffer.Buffer(timestamp_table, bin_dir)

for x in range(32):
    for z in range(32):
        chunk = get_chunk(x, z, buf)

        nbt = buffer.NBTBuffer(chunk.data, bin_dir)

        j = nbt.root.json()

        structures = j[""]["Level"]["Structures"]["Starts"]
        for k, v in structures.items():
            if v["id"] == "INVALID":
                continue

            chunk_x = v["ChunkX"]
            chunk_z = v["ChunkZ"]

            try:
                structure_x = v["Children"]["None"]["PosX"]
                structure_y = v["Children"]["None"]["PosY"]
                structure_z = v["Children"]["None"]["PosZ"]
            except KeyError:
                structure_x = chunk_x * 16
                structure_y = -1
                structure_z = chunk_z * 16

            r = f"r.{region_x}.{region_z}"
            c = f"c.{chunk_x}.{chunk_z}"
            print(f"X{structure_x:>6}, Y{structure_y:>4}, Z{structure_z:>6} ({r:<10}, {c:<10}) {k}")
