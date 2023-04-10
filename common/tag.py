import sys

from . import util

class TagID:
    End = 0
    Byte = 1
    Short = 2
    Int = 3
    Long = 4
    Float = 5
    Double = 6
    Byte_Array = 7
    String = 8
    List = 9
    Compound = 10
    Int_Array = 11
    Long_Array = 12

    strings = [
        "End",
        "Byte",
        "Short",
        "Int",
        "Long",
        "Float",
        "Double",
        "Byte_Array",
        "String",
        "List",
        "Compound",
        "Int_Array",
        "Long_Array",
    ]

    Numeric = [
        Byte,
        Short,
        Int,
        Long,
        Float,
        Double
    ]

    flat_json = [
        Byte,
        Short,
        Int,
        Long,
        Float,
        Double,
        String
    ]

    @staticmethod
    def to_string(id):
        try:
            return TagID.strings[id]
        except IndexError:
            print(f"Invalid tag id {id}")
            return ""

class Tag:
    def __init__(self, tag_id, length, name, payload, list_type=None):
        self.tag_id = tag_id
        self.length = length
        self.name = name
        self.payload = payload
        self.list_type = list_type

        self.filename = None

    def to_string(self, indent=0):
        s = f"Unimplemented output for id {self.tag_id}"
        if self.tag_id in TagID.Numeric:
            s = "TAG_{}({}): {}".format(
                TagID.to_string(self.tag_id),
                repr(self.name),
                self.payload
            )
        elif self.tag_id == TagID.Byte_Array:
            s = "TAG_{}({}): [{} bytes]".format(
                TagID.to_string(self.tag_id),
                repr(self.name),
                len(self.payload)
            )
        elif self.tag_id == TagID.String:
            s = "TAG_{}({}): '{}'".format(
                TagID.to_string(self.tag_id),
                repr(self.name),
                self.payload
            )
        elif self.tag_id == TagID.List:
            s = "TAG_{}({}): {} entries".format(
                TagID.to_string(self.tag_id),
                repr(self.name),
                len(self.payload)
            )
            s += "\n{}[".format('  '*indent)
            for tag in self.payload:
                s += "\n"
                s += '  '*(indent + 1)
                s += tag.to_string(indent=indent + 1)
            s += "\n{}]".format('  '*indent)
        elif self.tag_id == TagID.Compound:
            s = "TAG_{}({}): {} entries".format(
                TagID.to_string(self.tag_id),
                repr(self.name),
                len(self.payload)
            )
            s += "\n{}{{".format('  '*indent)
            for tag in self.payload:
                s += "\n"
                s += '  '*(indent + 1)
                s += tag.to_string(indent=indent + 1)
            s += "\n{}}}".format('  '*indent)
        else:
            print(f"Tag Unimplemented Tag: {TagID.to_string(self.tag_id)}")
            sys.exit(1)

        return s

    def to_json(self):
        return Tag._to_json(self)

    @staticmethod
    def _to_json(t, j={}):
        if t.tag_id in TagID.flat_json:
            n = f"{t.name}"
            j[n] = t.payload
        elif t.tag_id == TagID.Byte_Array:
            n = f"{t.name}"
            j[n] = f"[{len(t.payload)} bytes] @ {t.filename}"
        elif t.tag_id in [TagID.List, TagID.Int_Array, TagID.Long_Array]:
            n = f"{t.name}"
            j[n] = []
            a = j[n]
            for x in t.payload:
                Tag._to_json_unnamed(x, a)
        elif t.tag_id == TagID.Compound:
            n = f"{t.name}"
            j[n] = {}
            a = j[n]
            for x in t.payload:
                Tag._to_json(x, a)
        else:
            print(f"Json Unimplemented Tag: {TagID.to_string(t.tag_id)}")
            sys.exit(1)

        return j

    @staticmethod
    def _to_json_unnamed(t, j=[]):
        if t.tag_id in TagID.flat_json:
            j.append(t.payload)
        elif t.tag_id == TagID.Byte_Array:
            j.append(f"[{len(t.payload)} bytes] @ {t.filename}")
        elif t.tag_id in [TagID.List, TagID.Int_Array, TagID.Long_Array]:
            for x in t.payload:
                Tag._to_json_unnamed(x, j)
        elif t.tag_id == TagID.Compound:
            n = f"{t.name}"
            a = {}
            for x in t.payload:
                Tag._to_json(x, a)
            j.append(a)
        else:
            print(f"Json Unimplemented Tag: {TagID.to_string(t.tag_id)}")
            sys.exit(1)

            return j
