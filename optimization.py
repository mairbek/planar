import random
import logging
import math

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

        if min_y is not None and best_y == min_y:
            break

    return best_x, best_y


def hill_climb_optimize(domain, cost_fun):
    logger.debug("Going to perform hill climb optimization")

    y = None
    x = [random.randint(domain[i][0], domain[i][1])
         for i in range(len(domain))]

    while True:
        neighbors = []
        for j in range(len(domain)):
            if x[j] > domain[j][0]:
                n = x[0:j] + [x[j] + 1] + x[j + 1:]
                neighbors.append(n)
            if x[j] < domain[j][1]:
                n = x[0:j] + [x[j] - 1] + x[j + 1:]
                neighbors.append(n)

        current = cost_fun(x)
        best = current
        for  j in range(len(neighbors)):
            cost = cost_fun(neighbors[j])
            logger.debug("Hill climb cost=%s", cost)
            if cost < best:
                best = cost
                x = neighbors[j]

        logger.debug("Hill climb: x=%s, y=%s", x, best)

        if best == current or best == 0:
            y = best
            break

    return x, y


def annealing_optimize(domain, cost_function, T=1000000.0, cool=0.99999, step=1, min_y=0):
    x = [float(random.randint(domain[i][0], domain[i][1]))
         for i in range(len(domain))]
    y = None

    global_opt = None

    while T > 0.1:
        i = random.randint(0, len(domain) - 1)

        dir = random.randint(-step, step)

        vecb = x[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]:
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]:
            vecb[i] = domain[i][1]

        ea = cost_function(x)
        eb = cost_function(vecb)

        p = pow(math.e, (-eb - ea) / T)

        if eb < ea or random.random() < p:
            x = vecb
            y = eb

        if global_opt is None:
            global_opt = {"x": x, "y": y}
        elif global_opt["y"] > y:
            global_opt["x"] = x
            global_opt["y"] = y

        if min_y is not None and y == min_y:
            break

        T = T * cool

        logger.debug("x = %s, y = %s", x, y)

    if y > global_opt["y"]:
        x = global_opt["x"]
        y = global_opt["y"]

    return x, y
