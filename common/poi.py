import json

class POI:
    def __init__(self, region_name, name, cx, cz, x, y, z):
        _, rx, rz = region_name.split(".")

        self.name = name
        self.region_x = int(rx)
        self.region_z = int(rz)
        self.chunk_x = cx
        self.chunk_z = cz
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        s = "X{:>6}, Y{:>4}, Z{:>6} ({:<10} : {:<10}) {}"
        r = f"r.{self.region_x}.{self.region_z}"
        c = f"c.{self.chunk_x}.{self.chunk_z}"

        return s.format(self.x, self.y, self.z, r, c, self.name)

    def to_json(self):
        return {
            "name": self.name,
            "region_x": self.region_x,
            "region_z": self.region_z,
            "chunk_x": self.chunk_x,
            "chunk_z": self.chunk_z,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

class POISmall:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        s = "X{:>6}, Y{:>4}, Z{:>6} {}"

        return s.format(self.x, self.y, self.z, self.name)

    def to_json(self):
        return {
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "z": self.z
        }

class POIJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.to_json()
