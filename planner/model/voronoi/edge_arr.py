from translator import translate

class EdgeArray(object):

    EPSILON = 0.0001
    HUGE = 1000
    NEG_HUGE = -1000

    def __init__(self, voronoi, grid):
        self.pairs = []
        self.all_pts = []
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        for cell_i in xrange(0, len(voronoi)):
            cell = voronoi[cell_i]
            for face in cell['faces']:
                self.pairs.append([cell['vertices'][i] for i in face['vertices']])
        for pair in self.pairs:
            for row in xrange(0, self.height):
                self.all_pts.extend(self.intersect(pair[0], pair[1], [0, row], [self.width, row]))
        for point in self.all_pts:
            x = int(point[0])
            y = int(point[1])
            [i, j] = translate(x, y, [self.width, self.height])
            self.grid[i][j] = -2
            
    def highlight_path(self, path):
        pts = []
        for p_idx in xrange(1, len(path)):
            for row in xrange(0, self.height):
                pts.extend(self.intersect(path[p_idx - 1], path[p_idx], [0, row], [self.width, row]))
        for point in pts:
            x = int(point[0])
            y = int(point[1])
            [i, j] = translate(x, y, [self.width, self.height])
            self.grid[i][j] = -3
        
    def fclamp(self, flt):
        if flt < 0:
            return 0
        elif flt >= self.width:
            return self.width - 1
        return flt

    def intersect(self, p1, p2, q1, q2):
        '''
        p1 and p2 are two endpoints of a line segment
        q1 and q2 are two endponits of a row of viable space
        '''
        pts = []
        dx1 = p2[0] - p1[0]
        dx2 = q2[0] - q1[0]
        dy1 = p2[1] - p1[1]
        dy2 = q2[1] - q1[1]
        divzero = False
        try:
            slope1 = dy1 / dx1
        except ZeroDivisionError:
            slope1 = EdgeArray.HUGE
            divzero = True
        slope2 = dy2 / dx2
        if (abs(dx1) < EdgeArray.EPSILON):
            if ((q1[1] >= p1[1] and q1[1] <= p2[1]) or (q1[1] >= p2[1] and q1[1] <= p1[1])):
                pts.append([self.fclamp(p1[0]), q1[1]])
        elif divzero or abs(slope1) < EdgeArray.EPSILON:
            if int(p1[1]) == int(q1[1]):
                greater = p1
                lesser = p2
                if (p2[0] > p1[0]):
                    greater = p2
                    lesser = p1
                for col in xrange(int(lesser[0]), int(greater[0])):
                    pts.append([self.fclamp(col), q1[1]])
        else:
            x = ((q1[1] - p1[1]) / slope1) + p1[0]
            if ((x >= p1[0] and x <= p2[0]) or (x >= p2[0] and x <= p1[0])):
                if x >= 0 and x < self.width:
                    pts.append([self.fclamp(x), q1[1]])
        return pts