import random
import logging

logger = logging.getLogger("Optimization")

def random_optimize(domain, cost_fun, points=1000, max_y=(10 ** 8), min_y=0):
    logger.debug("going to optimize %s" % domain)
    best_y = max_y
    best_x = None

    for j in range(points):
        x = [random.randint(domain[i][0], domain[i][1])
             for i in range(len(domain))]

        logger.debug("\tCurrent configuration %s" % x)

        cost = cost_fun(x)

        logger.debug("\tCost %s", cost)

        if cost < best_y:
            best_y = cost
            best_x = x

        if min_y is not None and cost == min_y:
            break

    return best_x, best_y


def hill_climb_optimize(domain, cost_fun):
    pass