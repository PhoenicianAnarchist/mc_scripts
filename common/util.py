import gzip
import zlib
import sys

def xz_from_64(long):
    x_sign  = (long >> 31) & 0x1
    x_value =  long        & 0x7fffffff
    z_sign  = (long >> 63) & 0x1
    z_value = (long >> 32) & 0x7fffffff

    if x_sign:
        x_value -= (1 << 31)
    if z_sign:
        z_value -= (1 << 31)

    return x_value, z_value

def unpack_heightmap(long):
    vals = []

    for i in range(7):
        vals.append(long & 0b111111111)
        long >>= 9
        
    return vals

def range_map(x, fa, fb, ta, tb):
    scale = float(x - fa) / (fb - fa)
    return ta + (scale * (tb - ta))

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
