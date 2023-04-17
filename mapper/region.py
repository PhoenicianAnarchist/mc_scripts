import logging
from PIL import Image

from .chunk import Chunk

class Region:
    def __init__(self, json_dir, region_x, region_z, chunk_list):
        self.logger = logging.getLogger(__name__)

        self.json_dir = json_dir
        self.region_x = region_x
        self.region_z = region_z
        self.chunk_list = chunk_list

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating heightmap for region {self.region_x}, {self.region_z}")

        self.image = Image.new("L", (512, 512))

        for chunk in self.chunk_list:
            self.logger.debug(f"Generating chunk {chunk}")
            x, z = [int(x) for x in chunk.split(".")]
            c = Chunk(self.json_dir, self.region_x, self.region_z, x, z)
            m = c.generate_heightmap(heightmap)
            if m is None:
                self.logger.warning(f"Skipping chunk {chunk}")
                continue

            cx = x * 16
            cz = z * 16
            self.logger.debug(f"Pasting chunk {chunk} at {cx}, {cz}")
            self.image.paste(c.image, (cx, cz))

        return True
