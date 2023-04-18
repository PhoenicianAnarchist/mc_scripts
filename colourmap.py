#!/usr/bin/env python3
import argparse
import pathlib
import json
import sys
import logging

from common import util

import mapper

parser = argparse.ArgumentParser()
parser.add_argument("--config", default="./config.json", type=pathlib.Path)
parser.add_argument("--logfile", default="./log.log", type=pathlib.Path)
parser.add_argument("--json_dir", default="./data/extracted", type=pathlib.Path)
parser.add_argument("--output_dir", default="./data/maps", type=pathlib.Path)
parser.add_argument("--name", default=None)
parser.add_argument("-r", "--regions", nargs="*")
parser.add_argument("-c", "--chunks", nargs="*")
parser.add_argument("--force", action="store_true")
parser.add_argument("--loglevel", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="WARNING")
parser.add_argument("--heightmap", choices=["OCEAN_FLOOR", "WORLD_SURFACE", "MOTION_BLOCKING"], default="OCEAN_FLOOR")
args = parser.parse_args()

args.output_dir = pathlib.Path("./data/tmp")

## create log file
util.write(args.logfile, "")

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=args.logfile,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, args.loglevel)
)

try:
    with open(args.config, "r") as f:
        config = json.load(f)
except:
    logger.error(f"Error: Config file not found `{args.config}`")
    sys.exit(1)

for k, v in config.items():
    logger.debug(f"config.{k} == {v}")

if args.name is None:
    save_name = config["save_name"]
else:
    save_name = args.name

json_dir = args.json_dir.expanduser().resolve()
json_dir /= save_name
logger.debug(f"json_dir == {json_dir}")

output_dir = args.output_dir.expanduser().resolve()
output_dir /= save_name
logger.debug(f"output_dir == {output_dir}")

if not output_dir.exists():
    output_dir.mkdir(parents=True)

output_path = output_dir / "colourmap.png"
logger.debug(f"output_path == {output_path}")
if output_path.exists() and not args.force:
    logger.info(f"Skipping map for {save_name}: already generated")
    sys.exit(0)


if args.chunks is None:
    chunk_list = [f"{x}.{z}" for x in range(32) for z in range(32)]
else:
    chunk_list = args.chunks


logger.info(f"Generating heightmap {args.heightmap} for {save_name}")

region_x, region_z = [int(x) for x in args.regions[0].split(".")[1:]]
region_map = mapper.region.Region(
    json_dir, region_x, region_z, chunk_list=chunk_list
)
region_map.unpack_heightmap_data(args.heightmap)
colourmap = mapper.colour_map.ColourMap()
region_map.generate_colourmap(colourmap, args.heightmap)
logger.debug(f"saving colourmap for {save_name}")
region_map.colourmap.save(output_path)

# logger.info(f"Generating heightmap {args.heightmap} for {save_name}")
# level_map = mapper.level.Level(
#     json_dir, name=args.name, region_list=args.regions, chunk_list=args.chunks
# )
# level_map.unpack_heightmap_data(args.heightmap)
# colourmap = mapper.colour_map.ColourMap()
# level_map.generate_colourmap(colourmap, args.heightmap)
# logger.debug(f"saving colourmap for {save_name}")
# level.colourmap.save(output_path)
