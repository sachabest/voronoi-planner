# Voronoi Path Planning for Robotic Moevement

## CIS 391 Homework

Created bt Sacha Best, last modified 10/2016

### Overview

In this assignment, you will be creating an algorithm and visualization for calcuating paths through complex 3D spaces. THe goal is to use generalized Voronoi graphs to allow robots to autonomously move through buildings.

### Tasks

You will have several discree tasks to complete. In general, the steps fo complete the path planner include:

1. Read input file format and create a data structure to hold the read information.
2. Generate a Voronoi decomposition of the spaces
3. Convert the Voronoi decomposition into a graph with nodes and edges
4. Clean up the decomposition by removing edges that cross obstacles 
5. Given a start and end point, find the shortest path between the two
6. Draw (onscreen) the chosen path taken

### Tools

This assignment is created in Python. You are free to use standard Python modules to help augment your own code, but you cannot use specifically purposed libraries (i.e. voronoi-path-planner 0.1.0). SciPy and/or NumPy may be useful. 

### Input file format

You will be given a file containing the following information:

* first line: Dimensions of teh spaces (format: 100 500)
* Second line: Start and end points (format: x1 y1 x2 y2)
* Lines 3-n: points (in the bounding box) of obstacles (format: x y)

### Expected output

YOu are expected to output at least 4 images from iterations of the voronoi decomposition algorithm running on each given input file. You may output these as PNG image files in the same dimension as the given bounding box. 

Next, you should output the final path length between the start and end points (to the console is fine)

Finally, please output an image (similar to the decompositions) with the final path from start to end

### Provided code

For your convenience, we have provided a tool ```image_export.py``` that will output a PNG image given a 2D array of RGB color values. That is to say, your 2D array should be of tuples ``` (r, g, b) : 0 <= r, g, b <= 255 ```. See the example below:

```python
from image_export import rgb2png

with open("output.png", "wb") as f:
    f.write(rgb2png(source_arr))
```