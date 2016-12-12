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
            for p in line.get_points():
                self.line_events.push(p)

    def process(self):
        while not self.line_events.is_empty():
            if not self.circle_events.is_empty() and self.circle_events.peek().x <= self.line_events.peek().x:
                self.process_cirlce_event()
            else:
                self.process_line_event()

        # after all points, process remaining circle events
        while not self.circle_events.is_empty():
            self.process_cirlce_event()

        self.finish_edges()

    def process_line_event(self):
        p = self.line_events.pop()
        self.arc_insert(p)

    def process_cirlce_event(self):
        # get next event from circle pq
        e = self.circle_events.pop()

        if e.valid:
            # start new edge
            s = Segment(e.point)
            self.output.append(s)

            # remove associated arc (parabola)
            a = e.arc
            if a.left is not None:
                a.left.right = a.right
                a.left.seg_1 = s
            if a.right is not None:
                a.right.left = a.left
                a.right.seg_0 = s

            # finish the edges before and after a
            if a.seg_0 is not None: 
                a.seg_0.finish(e.point)
            if a.seg_1 is not None: 
                a.seg_1.finish(e.point)

            # recheck circle events on either side of p
            if a.left is not None: 
                self.check_circle_event(a.left, e.x)
            if a.right is not None: 
                self.check_circle_event(a.right, e.x)

    def arc_insert(self, para):
        if self.arc == None:
            self.arc = BTree(para)
            return
        
        arc_ptr = self.arc
        while arc_ptr is not None:
            isection = intersect(para, arc_ptr)
            if isection != None:
                isection2 = intersect(para, arc_ptr.right)

                # normal binary tree insertion here
                if arc_ptr.right != None and isection2 == None:
                    arc_ptr.right.left = BTree(arc_ptr.data, arc_ptr, arc_ptr.right)
                    arc_ptr.right = arc_ptr.right.left
                else:
                    arc_ptr.right = BTree(arc_ptr.data, arc_ptr)
                arc_ptr.right.seg_1 = arc_ptr.seg_1

                arc_ptr.right.left = BTree(para, arc_ptr, arc_ptr.right)
                arc_ptr.right = arc_ptr.right.left

                arc_ptr = arc_ptr.right # move dat pointer

                seg = Segment(isection)
                self.output.append(seg)
                arc_ptr.left.seg_1 = seg
                arc_ptr.seg_0 = seg

                # need 2 refs (half edge)
                seg = Segment(isection)
                self.output.append(seg)
                arc_ptr.right.seg_0 = seg
                arc_ptr.seg_1 = seg

                # check for new circle events around the new arc
                self.check_circle_event(arc_ptr, para.x)
                self.check_circle_event(arc_ptr.left, para.x)
                self.check_circle_event(arc_ptr.right, para.x)
                return
            arc_ptr = arc_ptr.right

        # insert at end if we need to
        arc_ptr = self.arc
        while arc_ptr.right is not None:
            arc_ptr = arc_ptr.right
        arc_ptr.right = BTree(para, arc_ptr)
        
        x = self.bounds[0]
        y = (arc_ptr.right.data.y + arc_ptr.data.y) / 2.0
        seg = Segment(Point(x, y))
        arc_ptr.seg_1 = seg
        arc_ptr.right.seg_0 = seg
        self.output.append(seg)

    def check_circle_event(self, arc, x0):
        # look for a new circle event for arc i
        if arc.e != None and arc.e.x != self.bounds[0]:
            arc.e.valid = False
        arc.e = None

        if arc.left == None or arc.right == None:
            return

        flag, x, o = circle(arc.left.data, arc.data, arc.right.data)
        if flag and x > self.bounds[0]:
            arc.e = Event(x, o, arc)
            self.circle_events.push(arc.e)

    def finish_edges(self):
        l = self.bounds[1] + (self.bounds[1] - self.bounds[0]) + (self.bounds[3] - self.bounds[2])
        i = self.arc
        while i.right is not None:
            if i.seg_1 is not None:
                p = parabola_intersection(i.data, i.right.data, l * 2.0)
                i.seg_1.finish(p)
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
            if p1 != None and p0 != None:
                res.append([[p0.x, p0.y], [p1.x, p1.y]])
        return res