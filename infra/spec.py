from fractions import Fraction

import StringIO

def parse_vertex(vertex):
    parts = vertex.split(',')
    return (Fraction(parts[0]), Fraction(parts[1]))

def parse_polygon(stream):
    n_vertices = int(stream.readline().strip())
    vertices = []
    for _ in range(n_vertices):
        vertices.append(parse_vertex(stream.readline().strip()))
    return vertices

def parse_spec(spec):
    stream = StringIO.StringIO(spec)
    n_polygons = int(stream.readline().strip())
    polygons = []
    for _ in range(n_polygons):
        polygons.append(parse_polygon(stream))
    n_edges = int(stream.readline().strip())
    edges = []
    for i in range(n_edges):
        edge = stream.readline().strip()
        points = [parse_vertex(x) for x in edge.split(' ')]
        edges.append(tuple(points))
    return {
        'polygons': polygons,
        'edges': edges
    }
