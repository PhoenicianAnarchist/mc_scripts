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

        self.chunks = None

    def unpack_heightmap_data(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Unpacking heightmap for region {self.region_x}, {self.region_z}")

        self.chunks = []
        for chunk in self.chunk_list:
            x, z = [int(x) for x in chunk.split(".")]
            c = Chunk(self.json_dir, self.region_x, self.region_z, x, z)
            m = c.unpack_heightmap_data(heightmap)
            if m is None:
                self.logger.warning(f"Skipping chunk {chunk}")
                continue

            self.chunks.append(c)

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating heightmap for region {self.region_x}, {self.region_z}")

        self.heightmap = Image.new("L", (512, 512))

        for chunk in self.chunks:
            chunk_name = f"{chunk.chunk_x}, {chunk.chunk_z}"
            self.logger.debug(f"Generating chunk {chunk_name}")
            cx = chunk.chunk_x * 16
            cz = chunk.chunk_z * 16
            self.logger.debug(f"Pasting chunk {chunk_name} at {cx}, {cz}")
            self.heightmap.paste(chunk.heightmap, (cx, cz))

        return True

    def generate_colourmap(self, colour_mapping, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Generating colourmap for region {self.region_x}, {self.region_z}")

        self.colourmap = Image.new("RGB", (512, 512))

        for chunk in self.chunks:
            chunk_name = f"{chunk.chunk_x}, {chunk.chunk_z}"
            self.logger.debug(f"Generating chunk {chunk_name}")
            try:
                chunk.generate_colourmap(colour_mapping)
            except IndexError as e:
                self.logger.error(f"Chunk generation failed {chunk_name}")
                continue

            cx = chunk.chunk_x * 16
            cz = chunk.chunk_z * 16
            self.logger.debug(f"Pasting chunk {chunk_name} at {cx}, {cz}")
            self.colourmap.paste(chunk.colourmap, (cx, cz))

        return True
