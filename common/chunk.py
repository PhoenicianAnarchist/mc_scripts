import gzip
import zlib

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

def to_index(offset, count):
    o = (offset * 4096)
    c = (count * 4096)
    return o, c

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
