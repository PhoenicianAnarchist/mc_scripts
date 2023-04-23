from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.slimes()

    def slimes(self):
        slimes = {
            "earth": (125, 248,  96),
            "ender": (176, 121, 224),
            "ichor": (321,  90,   0),
            "sky":   (122, 226, 223)
        }

        for slime, colour in slimes.items():
            self.map[f"tconstruct:{slime}_slime_tall_grass"] = colour
            self.map[f"tconstruct:{slime}_slime_fern"] = colour
            self.map[f"tconstruct:{slime}_vanilla_slime_grass"] = colour
            self.map[f"tconstruct:{slime}_congealed_slime"] = colour
            self.map[f"tconstruct:{slime}_slime_fluid"] = colour
