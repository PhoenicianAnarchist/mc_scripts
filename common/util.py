import gzip
import sys

def get_format(target_format, suffix_hint):
    if target_format == "auto":
        if suffix_hint in [".nbt", ".dat"]:
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

def read(filepath, format):
    if format == "nbt":
        data = read_raw(filepath)
    elif format == "dat":
        data = read_gzip(filepath)
    else:
        print(f"Unknown format: {format}")
        sys.exit(1)

    return data

def new_path(filepath, dir, suffix, mkdir=False):
    p = (filepath.parent.parent / dir / filepath.name).with_suffix(suffix)

    if (mkdir) and (not p.parent.is_dir()):
        p.parent.mkdir(parents=True)

    return p
