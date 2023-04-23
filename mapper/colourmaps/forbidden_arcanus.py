from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.woods()

    def woods(self):
        woods = {
            ## Wood Name:   [ planks, log, stripped, leaves ]
            "cherrywood":  [(212, 122, 84), (53, 32, 26), (144, 86, 62), (255, 163, 187)]
        }

        for wood, [planks, log, stripped, leaves] in woods.items():
            self.map[f"forbidden_arcanus:{wood}_button"] = planks
            self.map[f"forbidden_arcanus:{wood}_door"] = planks
            self.map[f"forbidden_arcanus:{wood}_fence"] = planks
            self.map[f"forbidden_arcanus:{wood}_fence_gate"] = planks
            self.map[f"forbidden_arcanus:{wood}_hanging_sign"] = planks
            self.map[f"forbidden_arcanus:{wood}_planks"] = planks
            self.map[f"forbidden_arcanus:{wood}_pressure_plate"] = planks
            self.map[f"forbidden_arcanus:{wood}_sign"] = planks
            self.map[f"forbidden_arcanus:{wood}_slab"] = planks
            self.map[f"forbidden_arcanus:{wood}_stairs"] = planks
            self.map[f"forbidden_arcanus:{wood}_trapdoor"] = planks

            self.map[f"forbidden_arcanus:{wood}_leaves"] = leaves
            self.map[f"forbidden_arcanus:{wood}_log"] = log
            self.map[f"forbidden_arcanus:{wood}_sapling"] = leaves
            self.map[f"forbidden_arcanus:{wood}_wood"] = log
            self.map[f"forbidden_arcanus:stripped_{wood}_log"] = stripped
            self.map[f"forbidden_arcanus:stripped_{wood}_wood"] = stripped
