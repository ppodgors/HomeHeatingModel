class Room:
    def __init__(self, row_min, row_max, col_min, col_max, function = None):
         self.row_min = row_min
         self.row_max = row_max
         self.col_min = col_min
         self.col_max = col_max
         self.func = function
         
    def y_len(self):
         return self.row_max - self.row_min
    
    def x_len(self):
         return self.col_max - self.col_min
    
    def x_min(self):
         return self.col_min
    
    def x_max(self):
         return self.col_max
    
    def y_min(self):
         return self.row_min
    
    def y_max(self):
         return self.row_max
    
    def init_fun(self):
         return self.func