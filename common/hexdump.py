class Hexer:
    def __init__(self, data, width=16):
        self.data = data
        self.width = width

        self.p = 0
        self.end = len(data)

    def __next__(self):
        if self.p >= self.end:
            raise StopIteration

        e = self.p + self.width
        if (self.p + self.width) >= self.end:
            e = self.end

        section = self.data[self.p:e]

        hex = []
        chars = ""
        for byte in section:
            hex.append(byte)
            if (byte >= ord(' ')) and (byte <= ord('~')):
                chars += chr(byte)
            else:
                chars += '.'

        h = ' '.join([f"{x:02x}" for x in hex])
        w = (self.width * 3) - 1
        s = f"{self.p:08x} : {h:{w}} : {chars}"

        self.p += self.width
        return s

    def __iter__(self):
        return self
