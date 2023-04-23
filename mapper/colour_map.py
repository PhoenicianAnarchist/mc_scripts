import logging
import json

from . import colourmaps

class ColourMap:
    map = {
        "DEFAULT": (255, 50, 255),
        "ERROR": (50, 255, 255)
    }

    transparent = []

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        for maps in colourmaps.maps:
            self.map.update(maps.map)
            self.transparent.extend(maps.transparent)

        new_transparent = []
        for t in self.transparent:
            if t not in self.map:
                new_transparent.append(t)

        self.logger.debug(f"Colour Map ({len(self.map)})\n{json.dumps(self.map, indent=2)}")
        self.logger.debug(f"Transparent ({len(self.transparent)})\n{json.dumps(self.transparent, indent=2)}")
        self.transparent = new_transparent
        self.logger.debug(f"New Transparent ({len(self.transparent)})\n{json.dumps(self.transparent, indent=2)}")

    def __getitem__(self, key):
        if key not in ColourMap.map:
            self.logger.error(f"No colour found for {key}")
            return ColourMap.map["DEFAULT"]

        return ColourMap.map[key]
