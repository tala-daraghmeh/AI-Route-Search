
import heapq
from itertools import count
from heuristic import heuristic


def search(graph, start, goal):
    if start not in graph or goal not in graph:
        return {'path': [], 'cost': None, 'steps': 0}

    if start == goal:
        return {'path': [start], 'cost': 0, 'steps': 1}

    counter = count()
    frontier = [(heuristic(graph, start, goal), start, next(counter), [start])]
    visited = set()
    steps = 0

    while frontier:
        h, city, _, path = heapq.heappop(frontier)

        if city in visited:
            continue

        visited.add(city)
        steps += 1

        if city == goal:
            total_cost = 0

            for current, next_city in zip(path, path[1:]):
                for neighbor, distance in graph[current]:
                    if neighbor == next_city:
                        total_cost += distance
                        break

            return {
                'path': path,
                'cost': total_cost,
                'steps': steps
            }

      

        for neighbor, distance in graph[city]:
            if neighbor not in visited:
                priority = heuristic(graph, neighbor, goal)
                heapq.heappush(
                    frontier,
                    (priority, neighbor, next(counter), path + [neighbor])
                )

    return {'path': [], 'cost': None, 'steps': steps}
