import json
import logging
from PIL import Image

class Chunk:
    def __init__(self, json_dir, region_x, region_z, chunk_x, chunk_z):
        self.logger = logging.getLogger(__name__)

        self.json_dir = json_dir
        self.region_x = region_x
        self.region_z = region_z
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.data = None

        region_name = f"r.{region_x}.{region_z}"
        filename = f"c.{chunk_x}.{chunk_z}.json"
        self.json_path = json_dir / "chunk_data" / region_name / filename

    def json_exists(self):
        if not self.json_path.exists():
            self.logger.warning(f"FileNotFound {self.json_path}")
            return False

        return True

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating heightmap for chunk {self.chunk_x}, {self.chunk_z}")

        if not self.json_path.exists():
            self.logger.warning(f"Skipping chunk {self.chunk_x}, {self.chunk_z}: file not found {self.json_path}")
            return None

        with open(self.json_path, "r") as f:
            data = json.load(f)

        j = data["Level"]["Heightmaps"]

        try:
            heightmap_ocean_floor = j[heightmap]
        except KeyError:
            self.logger.warning(f"Skipping chunk {self.chunk_x}, {self.chunk_z}: heightmap not found {heightmap}")
            return None

        ocean_floor = []
        for i, long in enumerate(heightmap_ocean_floor):
            self.logger.debug(f"Unpacking long {long}")
            vals = unpack_long(long)
            self.logger.debug(f"Got ints {vals}")
            if i == len(heightmap_ocean_floor) - 1:
                ocean_floor.extend(vals[:4])
            else:
                ocean_floor.extend(vals)

        self.image = Image.new("L", (16, 16))
        image_data = self.image.load()

        for z in range(16):
            for x in range(16):
                height = ocean_floor[x + (z * 16)]
                image_data[x, z] = height

        return True

def unpack_long(long):
    vals = []

    for i in range(7):
        vals.append(long & 0b111111111)
        long >>= 9

    return vals
