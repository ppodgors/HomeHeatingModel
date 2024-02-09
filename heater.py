class Heater:
    def __init__(self, horizontal, start_idx, length, position, room, level=1, exterior = True):
        self.horizontal = horizontal
        self.start_idx = start_idx
        self.length = length
        self.position = position
        self.level = level
        self.room = room
        self.exterior = exterior

    def coordinates(self):
        if self.exterior:
            return self.start_idx, self.start_idx + self.length, self.position
        else:
            return self.start_idx, self.start_idx + self.length, self.position+1

    def is_horizontal(self):
        return self.horizontal

    def room_nr(self):
        return self.room
    
    def get_level(self):
        return self.level