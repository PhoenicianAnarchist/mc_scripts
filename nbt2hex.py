#!/usr/bin/env python3
import argparse
import pathlib

from common import util

parser = argparse.ArgumentParser()

parser.add_argument("filepath")
parser.add_argument("-f", "--format", choices=["auto", "nbt", "dat"], default="auto")

args = parser.parse_args()

class Hexer:
    def __init__(self, data, width=16):
        self.data = data
        self.width = width

        self.p = 0
        self.end = len(data)

    def __next__(self):
        if self.p >= self.end:
            raise StopIteration

        e = self.p + self.width
        if (self.p + self.width) >= self.end:
            e = self.end

        section = self.data[self.p:e]

        hex = []
        chars = ""
        for byte in section:
            hex.append(byte)
            if (byte >= ord(' ')) and (byte <= ord('~')):
                chars += chr(byte)
            else:
                chars += '.'

        h = ' '.join([f"{x:02x}" for x in hex])
        w = (self.width * 3) - 1
        s = f"{self.p:08x} : {h:{w}} : {chars}"

        self.p += self.width
        return s

    def __iter__(self):
        return self

filepath = pathlib.Path(args.filepath).resolve()
filename = filepath.stem
suffix = filepath.suffix

hex_path = util.new_path(filepath, "hex", ".hex", mkdir=True)
nbt_path = util.new_path(filepath, "nbt", ".nbt", mkdir=True)
format = util.get_format(args.format, suffix)
data = util.read(filepath, format)

if filepath != nbt_path:
    util.write(nbt_path, data, "wb")

hexer = Hexer(data, width=16)
util.write(hex_path, "\n".join([line for line in hexer]))
