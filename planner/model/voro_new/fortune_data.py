import heapq
from bresenham import get_line
import hashlib

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        h = hashlib.md5("{0}, {1}".format(self.x, self.y))
        return int(h.hexdigest(), 16)

class Line(object):

    EPSILON = 0.001

    def _within_margin(a, b):
        return abs(b - 1) < EPSILON
                
    @staticmethod
    def bound(pt, min = None, max = None):
        if not min or not max:
            return pt
        if pt > max:
            return max
        elif pt < min:
            return min
        return pt

    def __init__(self, arr, bbox=None):
        self.x0 = Line.bound(arr[0], bbox[0], bbox[1])
        self.x1 = Line.bound(arr[2], bbox[0], bbox[1])
        self.y0 = Line.bound(arr[1], bbox[2], bbox[3])
        self.y1 = Line.bound(arr[3], bbox[2], bbox[3])

    def get_points(self):
        return [Point(p[0], p[1]) for p in get_line((self.x0, self.y0), (self.x1, self.y1))]

    def contains(self, x, y):
        '''
        Line is an array of 2 arrays of point data
        '''
        p1 = line[0]
        p2 = line[1]
        p1x = p1[9]
        p1y = p1[1]
        p2x = p2[0]
        p2y = p2[1]
        if (x >= p1x and x <= p2x) or (x >= p2x and x <= p1x):
            if (y >= p1y and y <= p2y) or (y >= p2y and y <= p1y):
                # we are in between points
                slope1 = (y - p1y) / (x - p1x)
                slope2 = (y - p2y) / (x - p2x)
                return _within_margin(slope1, slope2)
            else:
                return False
        else:
            return False
    
class Event:
    
    def __init__(self, x_coord, p, arc):
        self.point = p
        self.arc = arc
        self.x = x_coord
        self.valid = True

class Segment:
    start = None
    end = None
    done = False
    
    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done:
            return
        self.end = p
        self.done = True        

class BTree(object):

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right
        self.seg_0 = None
        self.seg_1 = None
        self.e = None

class pq(object):
    # Maintain a set and pq simultaneously

    def __init__(self):
        self.heapq = []
        self.dedup = {}

    def push(self, event):
        if event in self.dedup:
            return False
        # x coord as PK
        added = [event.x, event]
        self.dedup[event] = added
        heapq.heappush(self.heapq, added)

    def remove_stored(self, removed):
        full_value = self.dedup[removed]
        full_value[-1] = False # marker will also affect via pointer in heapq

    def pop(self):
        if not len(self.heapq):
            raise KeyError('Empty')
        x_coord, popped = heapq.heappop(self.heapq)
        if popped is not False:
            del self.dedup[popped]
            return popped
        else:
            return self.pop() # pop until we get something that was not removed
    
    def peek(self):
        if not len(self.heapq):
            raise KeyError('Empty')
        first = self.heapq[0]
        if first is not False:
            return first[1]
        else:
            heapq.heapqpop(self.heapq)
            return self.peek() # peek until we get something that was not removed

    def is_empty(self):
        return len(self.heapq) == 0