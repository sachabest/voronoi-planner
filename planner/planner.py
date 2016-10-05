#!/usr/bin/env python

from drawing.canvas import Canvas
from io.points import Reader
from model.binary import BinaryModel
from ui.canvas_painter import PathPainter

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

assert len(sys.argv) > 2
app = QApplication(sys.argv)
reader = Reader(sys.argv[1])
model = BinaryModel(reader.get_dimensions(), reader.get_points())
w = PathPainter(model)
sys.exit(app.exec_())