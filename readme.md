# MC Scripts

Various scripts to example and manipulate minecraft save data.

Versions tested:
- Java 1.16.5 (2586)

## chunk_extractor

Extracts chunk data and converts to JSON.
Specific regions and chunks can be specified, otherwise all will be extracted.

## structure_extractor

Parses JSON files saved by `chunk_extractor` and extracts structure types and locations.
Specific regions and chunks can be specified, otherwise all will be extracted.

## poi_extractor

Parses JSON files saved by `chunk_extractor` and extracts poi types and locations.
Specific regions and chunks can be specified, otherwise all will be extracted.

## region_heightmap

Parses JSON files saved by `chunk_extractor` and extracts heightmap data.
Saves individual files for each region.

## level_heightmap

Parses JSON files saved by `chunk_extractor` and extracts heightmap data.
Saves a single file containing all regions.
Regions can be specified in order to regenerate heightmap data (requires `--force` flag)
