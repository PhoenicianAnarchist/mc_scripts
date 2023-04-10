#!/usr/bin/env python3
import argparse
import pathlib
import json

from common import buffer
from common import tag
from common import util

parser = argparse.ArgumentParser()

parser.add_argument("filepath")
parser.add_argument("-f", "--format", choices=["auto", "nbt", "dat"], default="auto")

args = parser.parse_args()

filepath = pathlib.Path(args.filepath).resolve()
filename = filepath.stem
suffix = filepath.suffix

json_path = util.new_path(filepath, "json", ".json", mkdir=True)
bin_dir = util.new_path(filepath, f"bin/{filename}", ".bin", mkdir=True).parent
format = util.get_format(args.format, suffix)
data = util.read(filepath, format)

p = buffer.NBTBuffer(data, bin_dir)

j = tag.Tag._to_json(p.root)
util.write(json_path, json.dumps(j, indent=2))
