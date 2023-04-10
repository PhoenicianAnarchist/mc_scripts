#!/usr/bin/env python3
import argparse
import pathlib

from common import hexdump
from common import util

parser = argparse.ArgumentParser()

parser.add_argument("filepath")
parser.add_argument("-f", "--format", choices=["auto", "nbt", "dat"], default="auto")

args = parser.parse_args()

filepath = pathlib.Path(args.filepath).resolve()
filename = filepath.stem
suffix = filepath.suffix

hex_path = util.new_path(filepath, "hex", ".hex", mkdir=True)
nbt_path = util.new_path(filepath, "nbt", ".nbt", mkdir=True)
format = util.get_format(args.format, suffix)
data = util.read(filepath, format)

if filepath != nbt_path:
    util.write(nbt_path, data, "wb")

hexer = hexdump.Hexer(data, width=16)
util.write(hex_path, "\n".join([line for line in hexer]))
