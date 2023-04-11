#!/usr/bin/env python3
import argparse
import pathlib

from common import hexdump
from common import util

parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=pathlib.Path)
parser.add_argument("-f", "--format", choices=["auto", "nbt", "dat"], default="auto")
parser.add_argument("--output_dir", default="./data", type=pathlib.Path)
args = parser.parse_args()

filepath = args.filepath.resolve()
format = util.get_format(args.format, filepath.suffix)
data = util.read(filepath, format)

hexer = hexdump.Hexer(data, width=16)

hex_path = args.output_dir / "hex" / f"{filepath.stem}.hex"
util.write(hex_path, "\n".join([line for line in hexer]))
