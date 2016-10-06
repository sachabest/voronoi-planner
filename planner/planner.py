#!/usr/bin/env python

from drawing.canvas import Canvas
from io.points import Reader
from model.binary import BinaryModel
from model.voronoi.edge_arr import EdgeArray
from model.djikstra import DjikstraGraph
from ui.canvas_painter import PathPainter

import sys
import qdarkstyle
import random
import pyvoro
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pprint import pprint
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
vor_result = pyvoro.compute_2d_voronoi(model.obstacles,
    [[0, model.width() - 1], [0, model.height() - 1]], 2.0)
print 'model starting'

vor_model = EdgeArray(vor_result, model.grid)
print 'model complete'
djikstra = DjikstraGraph.from_voronoi(vor_result)
print djikstra.shortest_path(0, 1)
window = PathPainter(model)
sys.exit(app.exec_())
