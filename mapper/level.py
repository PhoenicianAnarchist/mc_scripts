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

    def generate_heightmap(self, heightmap="OCEAN_FLOOR"):
        img_w, img_h = self.get_map_size()
        self.image = Image.new("L", (img_w, img_h))
        self.logger.info(f"Generating heightmap for {self.name}")

        for region in self.region_list:
            region_name = region.name
            self.logger.debug(f"Generating region {region_name}")

            region_x, region_z = [int(x) for x in region_name.split(".")[1:]]

            r = Region(self.json_dir, region_x, region_z, self.chunk_list)
            m = r.generate_heightmap(heightmap)
            if m is None:
                self.logger.warning(f"Skipping region {region_name}")
                continue

            rx = (region_x - self.min_x) * 512
            rz = (region_z - self.min_z) * 512
            self.logger.debug(f"Pasting region {region_name} at {rx}, {rz}")
            self.image.paste(r.image, (rx, rz))

    def get_map_size(self):
        self.logger.info(f"Calculating map size...")

        region_x_coords = set()
        region_z_coords = set()

        for region in self.all_regions:
            region_x, region_z = [int(x) for x in region.name.split(".")[1:]]
            region_x_coords.add(region_x)
            region_z_coords.add(region_z)

        self.min_x = min(region_x_coords)
        self.min_z = min(region_z_coords)
        self.logger.debug(f"Minimum Region {self.min_x}, {self.min_z}")

        self.max_x = max(region_x_coords)
        self.max_z = max(region_z_coords)
        self.logger.debug(f"Maximum Region {self.max_x}, {self.max_z}")

        self.diff_x = self.max_x - self.min_x
        self.diff_z = self.max_z - self.min_z
        self.logger.debug(f"Region Range {self.diff_x}, {self.diff_z}")

        img_w = (self.diff_x + 1) * 512
        img_h = (self.diff_z + 1) * 512
        self.logger.debug(f"Pixels {img_w}, {img_h}")

        return img_w, img_h
