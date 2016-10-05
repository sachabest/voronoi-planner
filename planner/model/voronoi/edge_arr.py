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
            for pair in cell['adjacency']:
                self.pairs.append((cell['vertices'][pair[0]], cell['vertices'][pair[1]]))
            # for vert_i in xrange(1, len(voronoi[cell_i]['vertices'])):
            #     vert_prev = voronoi[cell_i]['vertices'][vert_i - 1]
            #     vert_next = voronoi[cell_i]['vertices'][vert_i]
            #     self.pairs.append((vert_prev, vert_next))
                # may need to close loop
        for pair in self.pairs:
            print pair
            for row in xrange(0, self.height):
                self.all_pts.extend(self.intersect(pair[0], pair[1], [0, row], [self.width, row]))
        for point in self.all_pts:
            x = int(point[1])
            y = int(point[0])
            y = self.height - y - 1
            self.grid[x][y] = -2
            
    def old_parser(self, voronoi_tuple, grid):
        self.verts = voronoi_tuple[0]
        self.lines = voronoi_tuple[1]
        self.edges = voronoi_tuple[2]
        self.grid = grid
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        all_pts = []
        print 'verts: ', self.verts
        print 'lines: ', self.lines
        print 'edges: ', self.edges

        for edge in self.edges:
            # ax + by = c
            a = self.lines[edge[0]][0]
            b = self.lines[edge[0]][1]
            c = self.lines[edge[0]][2]
            # first find min coords because the ilne could be infinite
            # we need two points of the line to use the intersect method
            p1 = []
            p2 = []
            if edge[1] == -1:
                # unbounded one direction
                if edge[2] == -1:
                    # unbounded both directions
                    if a > EdgeArray.EPSILON:
                        p1 = [EdgeArray.NEG_HUGE, int((c - (a * EdgeArray.NEG_HUGE)) / b)]
                        p2 = [EdgeArray.HUGE, int((c - (a * EdgeArray.HUGE)) / b)]
                    else:
                        p1 = [int((c - (b * EdgeArray.HUGE)) / a), EdgeArray.HUGE]
                        p2 = [int((c - (b * EdgeArray.NEG_HUGE)) / a), EdgeArray.NEG_HUGE]
                else:
                    p2 = self.verts[edge[2]]
                    if a > EdgeArray.EPSILON:
                        p1 = [EdgeArray.HUGE, int((c - (a * EdgeArray.HUGE)) / b)]
                    else:
                        p1 = [int((c - (b * EdgeArray.HUGE)) / a), EdgeArray.HUGE]
            else:
                if edge[2] == -1:
                    p2 = [int(x) for x in self.verts[edge[1]]]
                    if a > EdgeArray.EPSILON:
                        p1 = [EdgeArray.HUGE, int((c - (a * EdgeArray.HUGE)) / b)]
                    else:
                        p1 = [int((c - (b * EdgeArray.HUGE)) / a), EdgeArray.HUGE]
                else:
                    p2 = self.verts[edge[1]]
                    p1 = self.verts[edge[2]]
            p1 = [int(x) for x in p1]
            p2 = [int(x) for x in p2]
            print 'Line from {0} to {1}'.format(p1, p2)
            for row in xrange(0, self.height):
                all_pts.extend(self.intersect(p1, p2, [0, row], [self.width, row]))
        for point in all_pts:
            x = int(point[1])
            y = int(point[0])
            y = self.height - y - 1
            self.grid[x][y] = -2

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