
def circle(a, b, c):
    # check if bc is a "right turn" from ab
    if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0: return False, None, None

    # Joseph O'Rourke, Computational Geometry in C (2nd ed.) p.189
    A = b.x - a.x
    B = b.y - a.y
    C = c.x - a.x
    D = c.y - a.y
    E = A*(a.x + b.x) + B*(a.y + b.y)
    F = C*(a.x + c.x) + D*(a.y + c.y)
    G = 2*(A*(c.y - b.y) - B*(c.x - b.x))

    if (G == 0): return False, None, None # Points are co-linear

    # point o is the center of the circle
    ox = 1.0 * (D*E - B*F) / G
    oy = 1.0 * (A*F - C*E) / G

    # o.x plus radius equals max x coord
    x = ox + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)
    o = Point(ox, oy)
        
    return True, x, o
    
def intersect(p, i):
    # check whether a new parabola at point p intersect with arc i
    if (i is None): return False, None
    if (i.data.x0 == p.x0): return False, None

    a = 0.0
    b = 0.0

    if i.left is not None:
        a = (self.intersection(i.left.data, i.data, 1.0 * p.x)).y
    if i.right is not None:
        b = (self.intersection(i.data, i.right.data, 1.0 * p.x)).y

    if (((i.left is None) or (a <= p.y)) and ((i.right is None) or (p.y <= b))):
        py = p.y
        px = 1.0 * ((i.data.x)**2 + (i.data.y-py)**2 - p.x**2) / (2*i.data.x - 2*p.x)
        res = Point(px, py)
        return True, res
    return False, None

def intersection(p0, p1, l):
    # get the intersection of two parabolas
    p = p0
    if (p0.x == p1.x):
        py = (p0.y + p1.y) / 2.0
    elif (p1.x == l):
        py = p1.y
    elif (p0.x == l):
        py = p0.y
        p = p1
    else:
        # use quadratic formula
        z0 = 2.0 * (p0.x - l)
        z1 = 2.0 * (p1.x - l)

        a = 1.0/z0 - 1.0/z1
        b = -2.0 * (p0.y/z0 - p1.y/z1)
        c = 1.0 * (p0.y**2 + p0.x**2 - l**2) / z0 - 1.0 * (p1.y**2 + p1.x**2 - l**2) / z1

        py = 1.0 * (-b-math.sqrt(b*b - 4*a*c)) / (2*a)
        
    px = 1.0 * (p.x**2 + (p.y-py)**2 - l**2) / (2*p.x-2*l)
    res = Point(px, py)
    return res
