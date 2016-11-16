class Line(object):

    EPSILON = 0.001

    def _within_margin(a, b):
        return abs(b - 1) < EPSILON
        
    def __init__(self, arr, bbox=None):
        self.x0 = arr[0][0]
        self.x1 = arr[0][1]
        self.y0 = arr[1][0]
        self.y1 = arr[1][1]
        if bbox:
            if arr[0][0] > bbox[1][0]:
                self.x0 = bbox[1][0]
            if arr[0][0] < bbox[0][0]:
                self.x0 = bbox[0][0]
            if arr[1][0] > bbox[1][0]:
                self.x1 = bbox[1][0]
            if arr[1][0] < bbox[0][0]:
                self.x1 = bbox[0][0]
            if arr[0][1] > bbox[1][1]:
                self.y0 = bbox[1][1]
            if arr[0][1] < bbox[0][1]:
                self.y0 = bbox[0][1]
            if arr[1][1] > bbox[1][1]:
                self.y1 = bbox[1][1]
            if arr[1][1] < bbox[0][1]:
                self.y1 = bbox[0][1]

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
        self.x_coord = x_coord
        self.point = p
        self.arc = arc
        self.valid = True

class Arc:

    def __init__(self, p, a=None, b=None):
        self.oint = p
        self.pprev = a
        self.pnext = b
        self.e = None
        self.s0 = None
        self.s1 = None

class Segment:
    start = None
    end = None
    done = False
    
    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, p):
        if self.done: return
        self.end = p
        self.done = True        

class BTree(object):

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class pq(object):
    # Maintain a set and pq simultaneously

    def __init__(self):
        self.heapq = []
        self.dedup = {}

    def push(self, event):
        if event in self.dedeup:
            return False
        # x coord as PK
        added = [event[0], event]
        self.dedup[event] = added
        heapq.heapqpush(self.heapq, added)

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
            return first
        else:
            heapq.heapqpop(self.heapq)
            return self.peek() # peek until we get something that was not removed

    def is_empty(self):
        return len(self.heapq) == 0