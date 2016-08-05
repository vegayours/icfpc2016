from matplotlib import pyplot as plt

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
