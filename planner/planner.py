#!/usr/bin/env python

from drawing.canvas import Canvas
from io.points import Reader, LineReader
from model.line import LineModel
from model.binary import BinaryModel
from model.voronoi.edge_arr import EdgeArray
from model.djikstra import DjikstraGraph
from model.voro_new.fortune_list import Voronoi
from model.voro_new.fortune_data import Line
from model.spec.voronoi import Voronoi as v2
from ui.canvas_painter import PathPainter

import sys
import qdarkstyle
import random
import pyvoro
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pprint import pprint
# assert len(sys.argv) > 2
SAMPLE_SIZE = 10000
SIZE = 200
app = QApplication(sys.argv)
app.setStyleSheet(qdarkstyle.load_stylesheet(pyside=False))

if (len(sys.argv) > 1):
    # reader = Reader(sys.argv[1])
    line_reader = LineReader(sys.argv[1])
    model = LineModel(line_reader.get_dimensions(), line_reader.get_lines())
    # model = BinaryModel(reader.get_dimensions(), reader.get_points())
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
# lines = [Line(line, [0, model.width(), 0, model.height()]) for line in model.obstacles]
# raw_pts = set()
# for obs in lines:
#     for pt in obs.get_points():
#         raw_pts.add(pt)
# data = [[pt.x, pt.y] for pt in raw_pts]
# print data
# vor_result = pyvoro.compute_2d_voronoi(data,
#     [[0, model.width() ], [0, model.height() ]], 2.0)

vor_result = Voronoi(model.obstacles, [0, model.width(), 0, model.height()])
# vor_result = v2(model.obstacles)

vor_result.process()
print vor_result.get_output()
print 'model starting'
vor_model = EdgeArray(vor_result.get_output(), model.grid)
djikstra = DjikstraGraph.from_edge_arr(vor_model.pruned_pairs)
start = djikstra.nodes.keys()[0]
end = djikstra.nodes.keys()[-1]
(dist, path) = djikstra.shortest_path(start, end, translate=True)
vor_model.highlight_path(path)
print 'model complete'

window = PathPainter(model)
sys.exit(app.exec_())
