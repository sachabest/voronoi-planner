import cairocffi as cairo

class Canvas(object):

    def __init__(self, binary_model, out_file):
        self._surface = cairo.ImageSurface (cairo.FORMAT_ARGB32, binary_model.width(), 
            binary_model.height())
        self._ctx = cairo.Context(self._surface)
        self._ctx.set_source_rgb(1, 1, 1)
        self._ctx.rectangle(0, 0, binary_model.width(), binary_model.height())
        self._ctx.fill()
        self._ctx.set_line_width(0.5)
        self._ctx.set_source_rgb(0, 0, 0)
        for row_idx, row in enumerate(binary_model.grid):
            for col_idx, col in enumerate(binary_model.grid[row_idx]):
                x = binary_model.width() - col_idx
                y = binary_model.height() - row_idx
                if binary_model.grid[row_idx][col_idx] == -1:
                    print x, y, 'printing'
                    self._ctx.move_to(x, y)
                    self._ctx.line_to(x + 1, y + 1)
                    self._ctx.stroke()
        self._surface.write_to_png(out_file) # Output to PNG
