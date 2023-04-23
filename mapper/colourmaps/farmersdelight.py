from . import _map

class Map(_map.MapBase):
    def __init__(self):
        super().__init__()

    def generate(self):
        self.map["farmersdelight:canvas_rug"] = (184, 144, 96)
        self.map["farmersdelight:skillet"] = (36, 36, 36)

        self.crops(product_colour=False)

    def crops(self, product_colour=False):
        if product_colour:
            self.map["farmersdelight:wild_beetroots"] = (113, 21, 11)
            self.map["farmersdelight:wild_cabbages"] = (77, 140, 59)
            self.map["farmersdelight:wild_carrots"] = (255, 142, 9)
            self.map["farmersdelight:wild_onions"] = (172, 115, 47)
            self.map["farmersdelight:wild_potatoes"] = (217, 170, 81)
        else:
            self.map["farmersdelight:wild_beetroots"] = (74, 143, 40)
            self.map["farmersdelight:wild_cabbages"] = (241, 210, 67)
            self.map["farmersdelight:wild_carrots"] = (248, 241, 233)
            self.map["farmersdelight:wild_onions"] = (184, 120, 237)
            self.map["farmersdelight:wild_potatoes"] = (158, 92, 183)
