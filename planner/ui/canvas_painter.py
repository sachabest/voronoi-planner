from PyQt4.QtCore import *
from PyQt4.QtGui import *
from generated.ui_main import Ui_MainWindow

class PathPainter(QMainWindow):

    def __init__(self, binary_model):
        super(PathPainter, self).__init__()
        self._image = QImage(binary_model.width(), binary_model.height(), QImage.Format_RGB32)
        self.initUI()
        self.prepSaveImage(binary_model.grid)

    def colorMap(self, value):
        if value == -1:
            return (255, 0, 0)
        elif value == -2:
            return (0, 0, 0)
        elif value == -3:
            return (255, 0, 255)
        elif value == 0:
            return (0, 200, 200)
        return (0, 0, 0)

    def prepSaveImage(self, grid):
        for i in xrange(0, self._image.width()):
            for j in xrange(0, self._image.height()):
                value = qRgb(*self.colorMap(grid[i][j]))
                self._image.setPixel(i, j, value)
        self._scene.addPixmap(QPixmap.fromImage(self._image))
        self.ui.graphicsView.fitInView(self._scene.itemsBoundingRect(), Qt.KeepAspectRatio)

    def initUI(self):
        self.setWindowTitle("Voronoi Path Planning")
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._scene = QGraphicsScene(self)
        self.ui.graphicsView.setScene(self._scene)
        self.show()