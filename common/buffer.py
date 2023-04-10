import sys
import struct

from . import tag
from . import util

class Buffer:
    def __init__(self, data, bin_dir=None):
        self.data = data
        self.length = len(data)
        self.bin_dir = bin_dir

        self.reset()

    def reset(self):
        self.p = 0
        self.eof = False
        self.peek_past = False

    def peek(self, count):
        b = self.p
        e = self.p + count

        if e >= self.length:
            self.peek_past = True
            return self.data[b:]

        return self.data[b:e]

    def seek(self, pos):
        if pos >= self.length:
            self.p = self.length
            self.eof = True
        else:
            self.p = pos

        return (not self.eof)

    def read(self, count):
        data = self.peek(count)
        self.p = self.p + count

        if self.peek_past:
            self.eof = True
            self.p = self.length

        return data

    def ignore(self, count):
        self.read(count)
        return None


class NBTBuffer(Buffer):
    def __init__(self, data, bin_dir=None):
        super().__init__(data, bin_dir)
        self.__next__()

    def __iter__(self):
        return self

    def __next__(self):
        if self.eof:
            raise StopIteration

        tag_id = int.from_bytes(self.read(1), "big")

        if tag_id == tag.TagID.End:
            raise StopIteration

        self.root = self.consume_tag(tag_id)
        return self.root

    def get_name(self, nameless):
        if nameless:
            return (0, None)

        length = int.from_bytes(self.read(2), "big")
        name = self.read(length).decode()

        return (length, name)

    def consume_tag(self, tag_id, nameless=False):
        if tag_id == tag.TagID.Byte:
            return self.consume_integer(tag_id, 1, nameless=nameless)
        elif tag_id == tag.TagID.Short:
            return self.consume_integer(tag_id, 2, nameless=nameless)
        elif tag_id == tag.TagID.Int:
            return self.consume_integer(tag_id, 4, nameless=nameless)
        elif tag_id == tag.TagID.Long:
            return self.consume_integer(tag_id, 8, nameless=nameless)
        elif tag_id == tag.TagID.Float:
            return self.consume_float(nameless=nameless)
        elif tag_id == tag.TagID.Double:
            return self.consume_double(nameless=nameless)
        elif tag_id == tag.TagID.Byte_Array:
            return self.consume_byte_array(nameless=nameless)
        elif tag_id == tag.TagID.String:
            return self.consume_string(nameless=nameless)
        elif tag_id == tag.TagID.List:
            return self.consume_list(nameless=nameless)
        elif tag_id == tag.TagID.Compound:
            return self.consume_compound(nameless=nameless)
        elif tag_id == tag.TagID.Int_Array:
            return self.consume_int_array(nameless=nameless)
        elif tag_id == tag.TagID.Long_Array:
            return self.consume_long_array(nameless=nameless)

        else:
            print(f"Consume Unimplemented Tag: {tag.TagID.to_string(tag_id)} @ {self.p}")
            sys.exit(1)

    def consume_integer(self, tag_id, size, nameless=False):
        length, name = self.get_name(nameless)
        payload = int.from_bytes(self.read(size), "big", signed=True)

        return tag.Tag(tag_id, length, name, payload)

    def consume_float(self, nameless=False):
        length, name = self.get_name(nameless)
        payload = struct.unpack(">f", self.read(4))[0]

        return tag.Tag(tag.TagID.Float, length, name, payload)

    def consume_double(self, nameless=False):
        length, name = self.get_name(nameless)
        payload = struct.unpack(">d", self.read(8))[0]

        return tag.Tag(tag.TagID.Double, length, name, payload)

    def consume_byte_array(self, nameless=False):
        length, name = self.get_name(nameless)
        payload_length = int.from_bytes(self.read(4), "big")
        data = self.read(payload_length)

        if self.bin_dir is None:
            t = tag.Tag(tag.TagID.Byte_Array, length, name, b"")
            t.filename = ""

            return t

        filename = f"Byte_Array.{self.p}.hex"
        filepath = self.bin_dir / filename

        with open(filepath, "wb") as f:
            f.write(data)

        t = tag.Tag(tag.TagID.Byte_Array, length, name, data)
        t.filename = filename

        return t

    def consume_string(self, nameless=False):
        length, name = self.get_name(nameless)
        payload_length = int.from_bytes(self.read(2), "big")
        payload = self.read(payload_length).decode()

        return tag.Tag(tag.TagID.String, length, name, payload)

    def consume_list(self, nameless=False):
        length, name = self.get_name(nameless)

        payload_type = int.from_bytes(self.read(1), "big")
        list_length = int.from_bytes(self.read(4), "big")

        payload = []
        for i in range(list_length):
            payload.append(self.consume_tag(payload_type, nameless=True))

        return tag.Tag(tag.TagID.List, length, name, payload)

    def consume_compound(self, nameless=False):
        length, name = self.get_name(nameless)
        payload = [tag for tag in self]

        return tag.Tag(tag.TagID.Compound, length, name, payload)

    def consume_int_array(self, nameless=False):
        length, name = self.get_name(nameless)
        payload_length = int.from_bytes(self.read(4), "big")

        payload = []
        for i in range(payload_length):
            payload.append(self.consume_tag(tag.TagID.Int, nameless=True))

        return tag.Tag(tag.TagID.Int_Array, length, name, payload)

    def consume_long_array(self, nameless=False):
        length, name = self.get_name(nameless)
        payload_length = int.from_bytes(self.read(4), "big")

        payload = []
        for i in range(payload_length):
            payload.append(self.consume_tag(tag.TagID.Long, nameless=True))

        return tag.Tag(tag.TagID.Long_Array, length, name, payload)
