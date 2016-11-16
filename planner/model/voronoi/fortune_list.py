from fortune_data import *
from fortune_util import *

class Voronoi(object):
    def __init__(self, lines, size):
        self.output = [] # list of line segment
        self.lines = [Line(line, size) for line in lines]
        self.arc = None
        self.circle_events = pq() # circle events
        self.line_events = pq() # site events
        self.bounds = size
        for line in self.lines:
            self.line_events.push(line) # seed pq

    def process(self):
        while not self.line_events.is_empty():
            while not self.circle_events.is_empty():
                if self.circle_events.peek().x <= self.line_events.peek().x:
                # handle circl  e event with higher priority
                    self.process_circle_event()
            else:
                self.process_line_event() # handle site event

        # after all points, process remaining circle events
        while not self.circle_events.is_empty():
            self.process_circle_event()

        self.finish_edges()

    def process_line_event(self):
        p = self.lines.pop()
        self.arc_insert(p)

    def process_cirlce_event(self):
        # get next event from circle pq
        e = self.event.pop()

        if e.valid:
            # start new edge
            s = Segment(e.data)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.a
            if a.left is not None:
                a.left.right = a.right
                a.left.s1 = s
            if a.right is not None:
                a.right.left = a.left
                a.right.s0 = s

            # finish the edges before and after a
            if a.s0 is not None: 
                a.s0.finish(e.data)
            if a.s1 is not None: 
                a.s1.finish(e.data)

            # recheck circle events on either side of p
            if a.left is not None: 
                self.check_circle_event(a.left, e.x)
            if a.right is not None: 
                self.check_circle_event(a.right, e.x)

    def arc_insert(self, p):
        if self.arc is None:
            self.arc = BTree(p)
        else:
            # find the current arcs at p.y
            i = self.arc
            while i is not None:
                flag, z = intersect(p, i)
                if flag:
                    # new parabola intersects arc i
                    flag, zz = intersect(p, i.right)
                    if (i.right is not None) and (not flag):
                        i.right.left = Arc(i.data, i, i.right)
                        i.right = i.right.left
                    else:
                        i.right = Arc(i.data, i)
                    i.right.s1 = i.s1

                    # add p between i and i.right
                    i.right.left = Arc(p, i, i.right)
                    i.right = i.right.left

                    i = i.right # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    seg = Segment(z)
                    self.output.append(seg)
                    i.left.s1 = i.s0 = seg

                    seg = Segment(z)
                    self.output.append(seg)
                    i.right.s0 = i.s1 = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(i, p.x)
                    self.check_circle_event(i.left, p.x)
                    self.check_circle_event(i.right, p.x)

                    return
                        
                i = i.right

            # if p never intersects an arc, append it to the list
            i = self.arc
            while i.right is not None:
                i = i.right
            i.right = Arc(p, i)
            
            # insert new segment between p and i
            x = self.x0
            y = (i.right.data.y + i.data.y) / 2.0
            start = Point(x, y)

            seg = Segment(start)
            i.s1 = i.right.s0 = seg
            self.output.append(seg)

    def check_circle_event(self, i, x0):
        # look for a new circle event for arc i
        if (i.e is not None) and (i.e.x  <> self.x0):
            i.e.valid = False
        i.e = None

        if (i.left is None) or (i.right is None): return

        flag, x, o = circle(i.left.data, i.data, i.right.data)
        if flag and (x > self.x0):
            i.e = Event(x, o, i)
            self.event.push(i.e)

    def finish_edges(self):
        l = self.x1 + (self.x1 - self.x0) + (self.y1 - self.y0)
        i = self.arc
        while i.right is not None:
            if i.s1 is not None:
                p = intersection(i.data, i.right.data, l*2.0)
                i.s1.finish(p)
            i = i.right

    def print_output(self):
        it = 0
        for o in self.output:
            it = it + 1
            p0 = o.start
            p1 = o.end
            print (p0.x, p0.y, p1.x, p1.y)

    def get_output(self):
        res = []
        for o in self.output:
            p0 = o.start
            p1 = o.end
            res.append((p0.x, p0.y, p1.x, p1.y))
        return res