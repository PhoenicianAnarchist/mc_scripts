import json
import logging
from PIL import Image

from . import section

class Chunk:
    def __init__(self, json_dir, region_x, region_z, chunk_x, chunk_z):
        self.logger = logging.getLogger(__name__)

        self.json_dir = json_dir
        self.region_x = region_x
        self.region_z = region_z
        self.chunk_x = chunk_x
        self.chunk_z = chunk_z
        self.heightmap_data = None

        region_name = f"r.{region_x}.{region_z}"
        filename = f"c.{chunk_x}.{chunk_z}.json"
        self.json_path = json_dir / "chunk_data" / region_name / filename

    def json_exists(self):
        if not self.json_path.exists():
            self.logger.warning(f"FileNotFound {self.json_path}")
            return False

        return True

    def unpack_heightmap_data(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Unpacking heightmap {heightmap} for chunk {self.chunk_x}, {self.chunk_z}")

        if not self.json_path.exists():
            self.logger.warning(f"Skipping chunk {self.chunk_x}, {self.chunk_z}: file not found {self.json_path}")
            return None

        with open(self.json_path, "r") as f:
            self.chunk_data = json.load(f)

        j = self.chunk_data["Level"]["Heightmaps"]

        try:
            heightmap_data = j[heightmap]
        except KeyError:
            self.logger.warning(f"Skipping chunk {self.chunk_x}, {self.chunk_z}: heightmap not found {heightmap}")
            return None

        self.heightmap_data = []
        for i, long in enumerate(heightmap_data):
            self.logger.debug(f"Unpacking long {long}")
            vals = unpack_long(long)
            self.logger.debug(f"Got ints {vals}")
            if i == len(heightmap_data) - 1:
                self.heightmap_data.extend(vals[:4])
            else:
                self.heightmap_data.extend(vals)

        return True

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating heightmap {heightmap} for chunk {self.chunk_x}, {self.chunk_z}")

        if self.heightmap_data is None:
            self.unpack_heightmap_data(heightmap)

        self.heightmap = Image.new("L", (16, 16))
        image_data = self.heightmap.load()

        for z in range(16):
            for x in range(16):
                height = self.heightmap_data[x + (z * 16)]
                image_data[x, z] = height

        return True

    def generate_colourmap(self, colour_mapping, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating colourmap for chunk {self.chunk_x}, {self.chunk_z}")

        sections_data = self.chunk_data["Level"]["Sections"]
        sections = section.Sections(sections_data)

        if self.heightmap_data is None:
            self.unpack_heightmap_data(heightmap)

        self.colourmap = Image.new("RGB", (16, 16))
        image_data = self.colourmap.load()

        self.colour_map_data = []
        for z in range(16):
            for x in range(16):
                i = x + (z*16)
                y = self.heightmap_data[i] - 1

                try:
                    block = sections.get(x, y, z)
                    self.colour_map_data.append(block)
                except IndexError as e:
                    r = f"r.{self.region_x}.{self.region_z}"
                    c = f"c.{self.chunk_x}.{self.chunk_z}"
                    s = f"{r} {c} @ ({x}, {y}, {z})"
                    self.logger.error(f"Failed Get {s}")

                    s = []
                    for i in range(16):
                        s.append(json.dumps(self.heightmap_data[i*16:(i+1)*16]))
                    self.logger.error("Heightmap\n" + "\n".join(s))

                    s = []
                    for i in range(16):
                        c = self.colour_map_data[i*16:(i+1)*16]
                        s.append(json.dumps(c))
                    self.logger.error("Blocks\n" + "\n".join(s))

                    s = []
                    for i in range(16):
                        c = self.colour_map_data[i*16:(i+1)*16]
                        m = [colour_mapping[x] for x in c]
                        s.append(json.dumps(m))
                    self.logger.error("Colours\n" + "\n".join(s))

                    raise

                colour = colour_mapping[block]

                image_data[x, z] = colour

        return True

def unpack_long(long):
    vals = []

    for i in range(7):
        vals.append(long & 0b111111111)
        long >>= 9

    return vals
