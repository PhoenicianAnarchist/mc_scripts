class MapBase:
    def __init__(self):
        self.transparent = []
        self.map = {}

    def delete(self, key):
        self.map.pop(key)

    def rename(self, key, new):
        self.map[new] = self.map.pop(key)

    def generate(self):
        print(f"{__name__} not implimented generate()")
