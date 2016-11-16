'''
File format specification:

WIDTH HEIGHT
x y
x1 y1
...

'''

import logging

class LineReader(object):


    def __init__(self, filename):
        self._filename = filename
        self._raw = None
        with open(filename, 'r') as f:
            self._raw = f.read()
        self._lines = []
        self.width = 0
        self.height = 0
        self.logger = logging.getLogger(__name__)
        self._process()

    def _process(self):
        lines = self._raw.splitlines(True)
        first_line = lines[0].split(' ')
        if len(first_line) != 2:
            self.logger.error("Invalid input format for width and height infor.")
        [self.width, self.height] = first_line
        for line in lines[1:]:
            line_split = line.split(' ')
            if len(line_split) != 4:
                self.logger.error("Invalid input format for points.")
            else:
                self._lines.append((int(line_split[0]), int(line_split[1]), int(line_split[2]), int(line_split[3])))

    def get_dimensions(self):
        return (int(self.width), int(self.height))
    
    def get_lines(self):
        return self._lines

class Reader(object):

    def __init__(self, filename):
        self._filename = filename
        self._raw = None
        with open(filename, 'r') as f:
            self._raw = f.read()
        self._points = []
        self.width = 0
        self.height = 0
        self.logger = logging.getLogger(__name__)
        self._process()

    def _process(self):
        lines = self._raw.splitlines(True)
        first_line = lines[0].split(' ')
        if len(first_line) != 2:
            self.logger.error("Invalid input format for width and height infor.")
        [self.width, self.height] = first_line
        for line in lines[1:]:
            line_split = line.split(' ')
            if len(line_split) != 2:
                self.logger.error("Invalid input format for points.")
            else:
                self._points.append((int(line_split[0]), int(line_split[1])))

    def get_dimensions(self):
        return (int(self.width), int(self.height))
    
    def get_points(self):
        return self._points