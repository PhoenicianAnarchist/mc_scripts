#!/usr/bin/env python3
import argparse
import pathlib
import json

from common import buffer
from common import util

parser = argparse.ArgumentParser()
parser.add_argument("filepath", type=pathlib.Path)
parser.add_argument("-f", "--format", choices=["auto", "nbt", "dat"], default="auto")
parser.add_argument("--output_dir", default="./data", type=pathlib.Path)
parser.add_argument("--save_bin", action="store_true")
args = parser.parse_args()

filepath = pathlib.Path(args.filepath).resolve()
format = util.get_format(args.format, filepath.suffix)
data = util.read(filepath, format)

if args.save_bin:
    bin_dir = arg.output_dir / "bin"
else:
    bin_dir = None

p = buffer.NBTBuffer(data, bin_dir)
j = p.root.to_json()

json_path = args.output_dir / "json" / f"{filepath.stem}.json"
util.write(json_path, json.dumps(j, indent=2))
