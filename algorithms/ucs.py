
import heapq
from itertools import count


def search(graph, start, goal):
    if start not in graph or goal not in graph:
        return {'path': [], 'cost': None, 'steps': 0}

    if start == goal:
        return {'path': [start], 'cost': 0, 'steps': 0}

    counter = count()
    frontier = [(0, start, next(counter), [start])]
    visited = set()
    steps = 0

    while frontier:
        cost, city, _, path = heapq.heappop(frontier)

        if city in visited:
            continue

        if city == goal:
            return {
                'path': path,
                'cost': cost,
                'steps': steps
            }

        visited.add(city)
        steps += 1

        for neighbor, distance in graph[city]:
            if neighbor not in visited:
                new_cost = cost + distance

                heapq.heappush(
                    frontier,
                    (new_cost, neighbor, next(counter), path + [neighbor])
                )

    return {'path': [], 'cost': None, 'steps': steps}
