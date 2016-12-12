# some code adapted from original voronoi implementation at
# https://www.cs.hmc.edu/~mbrubeck/voronoi.html
# but not the main fortuen code, just the dependencies, like circle())

import math
from fortune_data import Point

''' output: (bool) match, (float) max x, (point) collision point'''
def circle(a, b, c):
    # check if bc is a "right turn" from ab
    if ((b.x - a.x)*(c.y - a.y) - (c.x - a.x)*(b.y - a.y)) > 0:
        return False, None, None

    # Joseph O'Rourke, Computational Geometry in C (2nd ed.) point.189
    A = b.x - a.x
    B = b.y - a.y
    C = c.x - a.x
    D = c.y - a.y
    E = A * (a.x + b.x) + B * (a.y + b.y)
    F = C * (a.x + c.x) + D * (a.y + c.y)
    G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

    if G == 0:
        return False, None, None # Points are co-linear

    # point o is the center of the circle
    ox = 1.0 * (D * E - B * F) / G
    oy = 1.0 * (A * F - C * E) / G

    # o.x plus radius equals max x coord
    x = ox + math.sqrt((a.x-ox)**2 + (a.y-oy)**2)        
    return True, x, Point(ox, oy)

def parabola_intersection(p0, p1, l):
    # marching stage
    p = p0
    if p0.x == p1.x:
        y = (p0.y + p1.y) / 2.0
    elif p1.x == l:
        y = p1.y
    elif p0.x == l:
        y = p0.y
        p = p1
    else:
        z0 = 2.0 * (p0.x - l)
        z1 = 2.0 * (p1.x - l)
        a = 1.0 / z0 - 1.0 / z1
        b = -2.0 * (p0.y / z0 - p1.y / z1)
        c = 1.0 * (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - 1.0 * (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1
        y = 1.0 * (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        
    x = 1.0 * (p.x ** 2 + (p.y - y) ** 2 - l ** 2) / (2 * p.x - 2 * l)
    return Point(x, y)

# does a parabola starting from "point" intersect the arc provided, and if so, where?
def intersect(point, arc):
    if arc == None or arc.data.x == point.x:
        return None

    a = 0.0
    b = 0.0
    
    if arc.left is not None:
        a = parabola_intersection(arc.left.data, arc.data, 1.0 * point.x).y
    if arc.right is not None:
        b = parabola_intersection(arc.data, arc.right.data, 1.0 * point.x).y

    if (arc.left == None or a <= point.y) and (arc.right == None or point.y <= b):
        y = point.y
        ydiff = arc.data.y - y
        x = 1.0 * (arc.data.x ** 2 + ydiff ** 2  - point.x ** 2) / (2 * arc.data.x - 2 * point.x)
        return Point(x, y)
    return None