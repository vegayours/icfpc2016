def detect_shift(polygons):
    points = [y for x in polygons for y in x]
    min_x = min(points,key=lambda i:i[0])
    min_y = min(points,key=lambda i:i[1])
    return min_x[0], min_y[1]
