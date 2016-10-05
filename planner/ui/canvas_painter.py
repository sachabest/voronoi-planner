from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PathPainter(QWidget):

    def __init__(self, binary_model):
        super(PathPainter, self).__init__()
        print "foo"
        self._image = QImage(binary_model.width(), binary_model.height(), QImage.Format_RGB32)
        self.resize(500, 500)
        self.prepSaveImage(binary_model.grid)
        self.initUI()
        

    def colorMap(self, value):
        if value == -1:
            print 'found'
            return (0, 0, 0)
        elif value == 0:
            return (255, 255, 255)
        return (0, 0, 0)

    def prepSaveImage(self, grid):
        for i in xrange(0, self._image.width()):
            for j in xrange(0, self._image.height()):
                value = qRgb(*self.colorMap(grid[i][j]))
                self._image.setPixel(i, j, value)

    def initUI(self):
        self.setWindowTitle("Voronoi Path Planning")
        self._label = QLabel(parent=self)
        self._label.setPixmap(QPixmap.fromImage(self._image))
        self.show()