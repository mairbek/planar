import logging
import optimization
from dataprovier import provide_graph
import view

def crosscount(coordinates, vertex, edge):
    logger = logging.getLogger("Crosscount")
    logger.debug("Current coordinates %s", coordinates)

    loc = dict([(vertex[i], (coordinates[i * 2], coordinates[i * 2 + 1])) for i in range(0, len(vertex))])
    logger.debug("locations %s", loc)
    total = 0

    for i in range(0, len(nodes)):
        for j in range(i+1, len(nodes)):
            logger.debug("%s %s", i, j)

            (x1, y1), (x2, y2) = loc[edge[i][0]], loc[edge[i][1]]
            (x3, y3), (x4, y4) = loc[edge[j][0]], loc[edge[j][1]]

            logger.debug("first edge %s {%s , %s}", edge[i], (x1, y1), (x2, y2))
            logger.debug("second edge %s {%s , %s}", edge[j], (x3, y3), (x4, y4))
            if are_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
                total += 1
    return total


def are_crossing(x1, y1, x2, y2, x3, y3, x4, y4):
    logger = logging.getLogger("are_crossing")

#    logger.debug("x1 %s", x1)
#    logger.debug("y1 %s", y1)
#    logger.debug("x2 %s", x2)
#    logger.debug("y2 %s", y2)
#    logger.debug("x3 %s", x3)
#    logger.debug("y3 %s", y3)
#    logger.debug("x4 %s", x4)
#    logger.debug("y4 %s", y4)

    den = 0.0 + (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    logger.debug("den %s", den)

    if den == 0:
        return False

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / den
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / den

    logger.debug("ua %s", ua)
    logger.debug("ub %s", ub)

    return ua > 0 and ua < 1 and ub > 0 and ub < 1


def cost_function(vertex, nodes):
    def func(v):
        return crosscount(v, vertex, nodes)

    return func

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    vertex = provide_graph()["vertex"]
    nodes = provide_graph()["nodes"]

    domain = [(10, 370)] * (len(vertex) * 2)

    logging.info(domain)

    (result_x, result_y) = optimization.random_optimize(domain, cost_function(vertex, nodes))

    logging.info("result (x=" + str(result_x) + " y=" + str(result_y) + ")")

    view.draw_graph(result_x, vertex, nodes)
#    are_crossing(314, 246, 164, 116, 312, 70, 25, 181)