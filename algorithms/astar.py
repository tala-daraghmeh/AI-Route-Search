"""A* Search implementation.

Interface:
    search(graph, start, goal) -> {'path': [...], 'cost': number, 'steps': int}
    graph: dict[str, list[tuple[str, number]]] (undirected adjacency list)
    No route: {'path': [], 'cost': None, 'steps': int}
    Goal test on frontier removal; expand each city at most once.
    Alpha tie-break, and steps count expanded nodes (per instructor).

How it works:
    f(n) = g(n) + h(n)
      g(n) = road distance (km) from the start to n
      h(n) = straight-line distance from n to the goal, rounded down
    The frontier is a priority queue of (f, city, g). The city name is the
    second item, so equal f values are broken alphabetically.
"""
import heapq
import math


def heuristic(graph, city, goal):
    """Straight-line distance from city to goal, rounded down (assignment rule)."""
    x1, y1 = graph.coordinates[city]
    x2, y2 = graph.coordinates[goal]
    return math.floor(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))


def search(graph, start, goal):
    frontier = [(heuristic(graph, start, goal), start, 0)]   # (f, city, g)
    best_g = {start: 0}      # cheapest known distance to each city
    parent = {start: None}   # to rebuild the path at the end
    expanded = set()
    steps = 0

    while frontier:
        f, city, g = heapq.heappop(frontier)
        if city in expanded:     # older, more expensive entry for this city
            continue

        expanded.add(city)
        steps += 1

        if city == goal:         # goal test on removal
            path = [goal]
            while parent[path[-1]] is not None:
                path.append(parent[path[-1]])
            path.reverse()
            return {'path': path, 'cost': g, 'steps': steps}

        for neighbor, km in sorted(graph[city]):     # alphabetical order
            new_g = g + km
            if neighbor not in expanded and new_g < best_g.get(neighbor, math.inf):
                best_g[neighbor] = new_g
                parent[neighbor] = city
                new_f = new_g + heuristic(graph, neighbor, goal)
                heapq.heappush(frontier, (new_f, neighbor, new_g))

    return {'path': [], 'cost': None, 'steps': steps}