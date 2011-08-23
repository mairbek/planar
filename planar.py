import logging
import math
import optimization
from dataprovier import provide_graph
from dataprovier import provide_plot_size
import view

logger = logging.getLogger("planar")

MIN_ANGLE = math.pi / 6.0

def crosscount(coordinates, vertex, edges, min_distance=50, min_angle=0):
    loc = dict([(vertex[i], (coordinates[i * 2], coordinates[i * 2 + 1])) for i in range(0, len(vertex))])
    total = 0

    for i in range(0, len(edges)):
        for j in range(i + 1, len(edges)):
            (x1, y1), (x2, y2) = loc[edges[i][0]], loc[edges[i][1]]
            (x3, y3), (x4, y4) = loc[edges[j][0]], loc[edges[j][1]]

            if are_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
                total += 1

    for i in range(len(vertex)):
        for j in range(i + 1, len(vertex)):
            (x1, y1), (x2, y2) = loc[vertex[i]], loc[vertex[j]]

            dist = math.sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))

            if dist > 0 and dist < min_distance:
                total += (1 - (dist / float(min_distance))) * 0.01

    for i in range(0, len(edges)):
        for j in range(i + 1, len(edges)):
            p = None
            if edges[i][0] == edges[j][0]:
                p = (edges[i][0], edges[i][1], edges[j][1])
            if edges[i][0] == edges[j][1]:
                p = (edges[i][0], edges[i][1], edges[j][0])
            if edges[i][1] == edges[j][0]:
                p = (edges[i][1], edges[i][0], edges[j][1])
            if edges[i][1] == edges[j][1]:
                p = (edges[i][1], edges[i][0], edges[j][0])

            if p is not None:
                points = [loc[p[i]] for i in range(3)]
                angle = calculate_angle(points)
                if angle > 0 and angle < min_angle:
                    total += (1 - (angle / float(min_angle))) * 0.01

    return total


def are_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
    den = 0.0 + (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    if not den:
        # parallel
        return False

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

    return ua > 0 and ua < 1 and ub > 0 and ub < 1


def distance(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def calculate_angle(p):
    a = distance(p[0], p[1])
    b = distance(p[1], p[2])
    c = distance(p[0], p[2])
    if not c or not a:
        return 0
    calc = (b ** 2 - a ** 2 - c ** 2) / (2 * a * c)
    if calc < 0:
        calc *= -1
    if calc > 1:
        # rounding problem
        logger.warn("rounding problem calc=%s" % calc)
        calc = 1
    return math.acos(calc)


def cost_function(vertex, edges):
    def func(v):
        return crosscount(v, vertex, edges)

    return func

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    vertex = provide_graph()["vertex"]
    edges = provide_graph()["edges"]

    plot = provide_plot_size()

    domain = []
    for i in range(len(vertex)):
        domain.append([10, plot[0] - 10])
        domain.append([10, plot[1] - 10])

    logging.info(domain)

    #    (result_x, result_y) = optimization.annealing_optimize(domain, cost_function(vertex, edges))
    (result_x, result_y) = optimization.genetic_optimization(domain, cost_function(vertex, edges))
    logging.info("result (x=" + str(result_x) + " y=" + str(result_y) + ")")

    view.draw_graph(result_x, vertex, edges, size=plot)
