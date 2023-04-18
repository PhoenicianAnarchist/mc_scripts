import logging

import json
import sys

class Sections:
    def __init__(self, sections_data):
        self.logger = logging.getLogger(__name__)
        self.sections = [None]*16

        for section_data in sections_data:
            section = Section(section_data)
            if section.section_y is None:
                continue

            section.unpack()

            self.sections[section.section_y] = section

    def get(self, x, y, z):
        self.logger.debug(f"Getting block for {x}, {y}, {z}")

        section_y = int(y / 16)
        self.logger.debug(f"section_y == {section_y}")

        y_offset = y % 16

        if self.sections[section_y] is None:
            raise IndexError(f"Invalid section {section_y}")

        return self.sections[section_y].get(x, y_offset, z)

class Section:
    def __init__(self, data):
        self.logger = logging.getLogger(__name__)
        self.section_y = data["Y"]
        self.data = None

        try:
            self.blockstates = data["BlockStates"]
            self.palette = data["Palette"]
        except KeyError:
            self.logger.warning(f"No data for section {self.section_y}")
            self.blockstates = None
            self.palette = None
            self.section_y = None

    def get(self, x, y, z):
        self.logger.debug(f"Getting block for {x}, {y}, {z}")

        index = self.data[x + (z*16) + (y*256)]
        self.logger.debug(f"index == {index}")

        try:
            block = self.palette[index]["Name"]
        except IndexError:
            c = f"({x}, {(self.section_y * 16) + y}, {z})"
            self.logger.error(f"self.palette IndexError {index} @ {c}")
            j = json.dumps(self.palette, indent=2)
            self.logger.error(f"length == {len(self.palette)}\n{j}")

            states = []
            for z in range(16):
                for x in range(16):
                    i = x + (z*16)
                    d = self.slices[y][i]
                    states.append(d)

            s = []
            for i in range(16):
                c = states[i*16:(i+1)*16]
                s.append(json.dumps(c))
            self.logger.error("Blockstates\n" + "\n".join(s))

            return "ERROR"

        self.logger.debug(f"block == {block}")

        return block

    def unpack(self):
        self.logger.info(f"Unpacking Section Data for Y={self.section_y}")
        bits = (len(self.palette) - 1).bit_length()
        mask = 2 ** bits
        self.logger.debug(f"bits == {bits}, mask == {mask}")

        if len(self.palette) == 1:
            self.data = [0]*4096
        else:
            self.data = []
            for long in self.blockstates:
                self.logger.debug(f"Unpacking long {long}")
                vals = unpack_long(long, bits)
                self.logger.debug(f"Got ints {vals}")
                self.data.extend(vals)

        self.data = self.data[:4096]

        self.slices = []
        for i in range(16):
            self.slices.append(self.data[i*256:(i+1)*256])


def unpack_long(long, bits):
    vals = []
    mask = (2 ** bits) - 1

    m = int(64/bits)
    for i in range(m):
        vals.append(long & mask)
        long >>= bits

    return vals
