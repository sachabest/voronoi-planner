
class Obstacle(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '({0}. {1})'.format(self.x, self.y)

class BinaryModel(object):

    def __init__(self, dimensions, obstacles):
        self._dimensions = dimensions
        self.obstacles = []
        self.grid = [[0 for i in range(0, self._dimensions[1])] for j in range(0, self._dimensions[1])]
        for obstacle in obstacles:
            self._add_obstacle(obstacle)
        
    def width(self):
        return self._dimensions[0]
    
    def height(self):
        return self._dimensions[1]
    
    def _add_obstacle(self, tup):
        x = tup[0]
        y = tup[1]
        self.obstacles.append(Obstacle(x, y))
        assert y < self.height()
        assert x < self.width()
        x = self._dimensions[0] - x - 1
        y = self._dimensions[1] - y - 1
        self.grid[y][x] = -1