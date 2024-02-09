class Door:
    def __init__(self, horizontal, start_idx, length, position, room):
        self.horizontal = horizontal
        self.start_idx = start_idx
        self.length = length
        self.position = position
        self.room = room

    def coordinates(self):
        return self.start_idx, self.start_idx + self.length, self.position
        
    def is_horizontal(self):
        return self.horizontal

    def room_nr(self):
        return self.room