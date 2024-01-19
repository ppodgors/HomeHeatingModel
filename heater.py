class Heater:
    def __init__(self, horizontal, start_idx, length, position):
        self.horizontal = horizontal
        self.start_idx = start_idx
        self.length = length
        self.position = position

    def coordinates(self):
        return self.start_idx, self.start_idx + self.length, self.position
        
    def is_horizontal(self):
        return self.horizontal
