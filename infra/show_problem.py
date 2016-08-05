from matplotlib import pyplot as plt
import sys
import json
import spec

def detect_shift(polygons):
    points = [y for x in polygons for y in x]
    min_x = min(points,key=lambda i:i[0])
    min_y = min(points,key=lambda i:i[1])
    return min_x[0], min_y[1]

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
    spec_str = problem['spec']
    parsed = spec.parse_spec(spec_str)
    print "Polygons:", len(parsed['polygons'])
    for point in parsed['polygons'][0]:
        print "{},{}".format(point[0], point[1])

    shift = detect_shift(parsed['polygons'])
    print 'Shift: ', shift
    show_skeleton(parsed['edges'], shift)
