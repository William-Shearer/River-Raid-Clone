class Vector2:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return f"X_pos: {self._x}, Y_pos: {self._y}"
    
    def __del__(self):
        pass
    
    @property
    def coord_x(self):
        return self._x
    
    def set_x(self, increment):
        self._x += increment

    @property
    def coord_y(self):
        return self._y
    
    def set_y(self, increment):
        self._y += increment

    