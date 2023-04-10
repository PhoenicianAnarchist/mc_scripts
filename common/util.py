import gzip
import zlib
import sys

def get_format(target_format, suffix_hint):
    if target_format == "auto":
        if suffix_hint in [".nbt", ".dat", ".zlib"]:
            return suffix_hint.strip(".")
        else:
            print(f"Unknown suffix: {suffix_hint}")
            sys.exit(1)

    return target_format

def read_raw(filepath):
    data = ""
    with open(filepath, "rb") as f:
        data = f.read()
    return data

def read_gzip(filepath):
    data = ""
    with gzip.open(filepath, "rb") as f:
        data = f.read()
    return data

def read_zlib(filepath):
    data = ""
    with open(filepath, "rb") as f:
        data = zlib.decompress(f.read())
    return data

def read(filepath, format):
    if format == "nbt":
        data = read_raw(filepath)
    elif format == "dat":
        data = read_gzip(filepath)
    elif format == "zlib":
        data = read_zlib(filepath)
    else:
        print(f"Unknown format: {format}")
        sys.exit(1)

    return data

def write(filepath, data, mode="w"):
    if not filepath.parent.is_dir():
        filepath.parent.mkdir(parents=True)

    with open(filepath, mode) as f:
        f.write(data)

def new_path(filepath, dir, suffix, mkdir=False):
    p = filepath.parent.parent / dir / filepath.name
    return p.with_suffix(suffix)
