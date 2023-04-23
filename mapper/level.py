import logging
from PIL import Image

from .region import Region

class Level:
    def __init__(self, json_dir, name=None, region_list=None, chunk_list=None):
        self.logger = logging.getLogger(__name__)

        self.json_dir = json_dir

        if name is None:
            self.name = json_dir.name
        else:
            self.name = name

        region_dir = json_dir / "chunk_data"
        dirs = sorted((region_dir).iterdir())
        self.all_regions = [x for x in dirs if x.stem.startswith("r")]
        self.logger.debug(f"Found region directories in {region_dir}: {[x.name for x in self.all_regions]}")

        if region_list is None:
            self.region_list = self.all_regions
        else:
            sub_dir = json_dir / "chunk_data"
            self.region_list = [sub_dir / r for r in region_list]

        if chunk_list is None:
            self.chunk_list = [f"{x}.{z}" for x in range(32) for z in range(32)]
        else:
            self.chunk_list = chunk_list

        self.region_data = None

        self.range = None
        self.image_width = None
        self.image_height = None
        self.region_x_offset = None
        self.region_z_offset = None
        self.calculate_map_size()

    def unpack_heightmap_data(self, heightmap="OCEAN_FLOOR"):
        self.logger.info(f"Unpacking heightmap for {self.name}")

        if self.region_data is not None:
            return

        self.region_data = []
        for region in self.region_list:
            region_name = region.name
            self.logger.debug(f"Generating region {region_name}")

            x, z = [int(x) for x in region.name.lstrip("r.").split(".")]

            r = Region(self.json_dir, x, z, self.chunk_list)
            m = r.unpack_heightmap_data(heightmap)
            if m is None:
                self.logger.warning(f"Skipping region {region_name}")
                continue

            self.region_data.append(r)

        self.logger.debug(f"{len(self.region_data)} regions unpacked")

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        self.heightmap = Image.new("L", (self.image_width, self.image_height))
        self.logger.info(f"Generating heightmap for {self.name}")

        if self.region_data is None:
            self.unpack_heightmap_data(heightmap)

        for region in self.region_data:
            region_name = f"r.{region.region_x}.{region.region_z}"
            self.logger.debug(f"Generating region {region_name}")

            m = region.generate_heightmap(heightmap)
            if m is None:
                self.logger.warning(f"Skipping region {region_name}")
                continue

            rx = (region.region_x - self.region_x_offset) * 512
            rz = (region.region_z - self.region_z_offset) * 512
            self.logger.debug(f"Pasting region {region_name} at {rx}, {rz}")
            self.heightmap.paste(region.heightmap, (rx, rz))

    def generate_colourmap(self, colour_mapping, heightmap="OCEAN_FLOOR"):
        self.colourmap = Image.new("RGB", (self.image_width, self.image_height))
        self.logger.info(f"Generating heightmap for {self.name}")

        if self.region_data is None:
            self.unpack_heightmap_data(heightmap)

        for region in self.region_data:
            region_name = f"r.{region.region_x}.{region.region_z}"
            self.logger.debug(f"Generating region {region_name}")

            m = region.generate_colourmap(colour_mapping, heightmap)
            if m is None:
                self.logger.warning(f"Skipping region {region_name}")
                continue

            rx = (region.region_x - self.region_x_offset) * 512
            rz = (region.region_z - self.region_z_offset) * 512
            self.logger.debug(f"Pasting region {region_name} at {rx}, {rz}")
            self.colourmap.paste(region.colourmap, (rx, rz))

    def calculate_map_size(self):
        self.logger.info(f"Calculating map size...")

        region_x_coords = set()
        region_z_coords = set()

        for region in self.region_list:
            x, z = [int(x) for x in region.name.lstrip("r.").split(".")]
            region_x_coords.add(x)
            region_z_coords.add(z)

        min_x = min(region_x_coords)
        min_z = min(region_z_coords)
        self.logger.debug(f"Minimum Region {min_x}, {min_z}")

        max_x = max(region_x_coords)
        max_z = max(region_z_coords)
        self.logger.debug(f"Maximum Region {max_x}, {max_z}")

        diff_x = max_x - min_x
        diff_z = max_z - min_z
        self.logger.debug(f"Region Range {diff_x}, {diff_z}")

        img_w = (diff_x + 1) * 512
        img_h = (diff_z + 1) * 512
        self.logger.debug(f"Pixels {img_w}, {img_h}")

        self.image_width = img_w
        self.image_height = img_h
        self.region_x_offset = min_x
        self.region_z_offset = min_z

        a = f"{min_x}.{min_z}"
        b = f"{max_x}.{max_z}"

        if a == b:
            self.range = a
        else:
            self.range = f"{a}-{b}"
