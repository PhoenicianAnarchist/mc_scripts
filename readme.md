# MC Scripts

Various scripts to example and manipulate minecraft save data.

## nbt2hex

A simple hex dumper.

Automatically detects file format from extension, but format can be specified:
- `nbt`: uncompressed
- `dat`: compressed with gzip

## nbt2json

Converts an NBT file to JSON.

Automatically detects file format from extension, but format can be specified:
- `nbt`: uncompressed
- `dat`: compressed with gzip

## chunk_extractor

Extracts chunk data and converts to JSON.
Specific regions and chunks can be specified, otherwise all will be extracted.

## dump_structures

Parses region files within a save and extracts structure types and locations.

## dump_poi

Parses poi files within a save and extracts poi types and locations.