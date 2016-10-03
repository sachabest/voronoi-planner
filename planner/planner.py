#!/usr/bin/env python

from drawing.canvas import Canvas
from io.points import Reader
from model.binary import BinaryModel

import sys

def main():
    assert len(sys.argv) > 2
    reader = Reader(sys.argv[1])
    model = BinaryModel(reader.get_dimensions(), reader.get_points())
    canvas = Canvas(model, sys.argv[2])

if __name__ == '__main__':
    main()