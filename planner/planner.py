#!/usr/bin/env python

from drawing.canvas import Canvas
from io.points import Reader
from model.binary import BinaryModel
from model.voronoi.fortune import computeVoronoiDiagram
from model.voronoi.edge_arr import EdgeArray
from ui.canvas_painter import PathPainter

import sys
import qdarkstyle
import random
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# assert len(sys.argv) > 2
SAMPLE_SIZE = 3000
SIZE = 200
app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

if (len(sys.argv) > 1):
    reader = Reader(sys.argv[1])
    model = BinaryModel(reader.get_dimensions(), reader.get_points())
else:
    dimensions = (SIZE, SIZE)
    points = []
    count = 0
    while count < SIZE ** 2:
        f = random.uniform(0, 1)
        if f <= float(1.0 / SAMPLE_SIZE):
            points.append((int(count / SIZE), count % SIZE))
        count += 1
    model = BinaryModel(dimensions, points)
vor_result = computeVoronoiDiagram(model.obstacles)
print 'model starting'
vor_model = EdgeArray(vor_result, model.grid)
print 'model complete'
window = PathPainter(model)
sys.exit(app.exec_())
