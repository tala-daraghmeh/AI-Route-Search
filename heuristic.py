
import math
def heuristic(graph, city, goal):
    x1, y1 = graph.coordinates[city]
    x2, y2 = graph.coordinates[goal]

    dx = x1 - x2
    dy = y1 - y2

    result = math.sqrt(dx * dx + dy * dy)
    return math.floor(result)