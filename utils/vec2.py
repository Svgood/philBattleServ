class Vec2:

    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def add(self, vec):
        self.x += vec.x
        self.y += vec.y