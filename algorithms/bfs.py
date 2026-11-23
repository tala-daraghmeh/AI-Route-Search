"""BFS implementation placeholder. This belongs to the assigned team member.

Interface:
    search(graph, start, goal) -> {'path': [...], 'cost': number, 'steps': int}
    graph: dict[str, list[tuple[str, number]]] (undirected adjacency list)
    No route: {'path': [], 'cost': None, 'steps': int}
    Goal test on frontier removal; expand each city at most once.
    Alpha tie-break, and steps count expanded nodes (per instructor).
"""



from collections import deque


def search(graph, start, goal):
    queue = deque([(start, [start], 0)])
    visited = set()
    steps = 0

    while queue:
        city, path, cost = queue.popleft()

        if city in visited:
            continue

        visited.add(city)
        steps += 1

        if city == goal:
            return {
                "path": path,
                "cost": cost,
                "steps": steps
            }

        for neighbor, distance in sorted(graph[city]):
            if neighbor not in visited:
                queue.append((
                    neighbor,
                    path + [neighbor],
                    cost + distance
                ))

    return {
        "path": [],
        "cost": None,
        "steps": steps
    }




