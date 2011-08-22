import logging
import math
import optimization
from dataprovier import provide_graph
from dataprovier import provide_plot_size
import view

logger = logging.getLogger("planar")

def crosscount(coordinates, vertex, edges, min_distance=50):
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

            if dist < min_distance:
                total += (1 - (dist / float(min_distance)))

    return total


def are_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
    den = 0.0 + (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)

    if not den:
        # parallel
        return False

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

    return ua > 0 and ua < 1 and ub > 0 and ub < 1


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