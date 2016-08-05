from matplotlib import pyplot as plt
import sys
import json
import StringIO
from fractions import Fraction

def parse_vertex(vertex):
    parts = vertex.split(',')
    return (Fraction(parts[0]), Fraction(parts[1]))

def parse_polygon(stream):
    n_vertices = int(stream.readline().strip())
    vertices = []
    for i in range(n_vertices):
        vertices.append(parse_vertex(stream.readline().strip()))
    return vertices

def detect_shift(polygons):
    points = [y for x in polygons for y in x]
    min_x = min(points,key=lambda i:i[0])
    min_y = min(points,key=lambda i:i[1])
    return min_x[0], min_y[1]

def parse_spec(stream):
    n_polygons = int(stream.readline().strip())
    polygons = []
    for i in range(n_polygons):
        polygons.append(parse_polygon(stream))
    n_edges = int(stream.readline().strip())
    edges = []
    for i in range(n_edges):
        edge = stream.readline().strip()
        points = [parse_vertex(x) for x in edge.split(' ')]
        edges.append(tuple(points))
    return {
        'silueth': polygons,
        'skeleton': edges
    }

def show_skeleton(skel, shift):
    x_poins = []
    y_poins = []
    for edge in skel:
        x, y = zip(*list(edge))
        x = [i - shift[0] for i in x]
        y = [i - shift[1] for i in y]
        x_poins.extend(x)
        y_poins.extend(y)
        plt.plot(x, y)
    plt.xlim([-0.5, 1.5])
    plt.ylim([-0.5, 1.5])
    plt.show()

if __name__ == '__main__':
    problem = json.load(open(sys.argv[1]))
    spec = problem['spec']
    stream = StringIO.StringIO(spec)
    parsed = parse_spec(stream)
    print "Polygons:", len(parsed['silueth'])
    for i in parsed['silueth'][0]:
        print "{},{}".format(i[0], i[1])

    shift = detect_shift(parsed['silueth'])
    print 'Shift: ', shift
    show_skeleton(parsed['skeleton'], shift)
