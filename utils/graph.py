"""Map validation and adjacency representation for the team search algorithms."""
import math

class MapValidationError(ValueError):
    pass


def prepare_map(data):
    """Validate a map and return normalized map + undirected adjacency list.

    The coordinates are in km; roads are bidirectional. Keep alphabetical
    neighbors so the algorithms can implement deterministic tie handling.
    """
    if not isinstance(data, dict):
        raise MapValidationError('Map must be a JSON object.')
    if not isinstance(data.get('cities'), list) or not data['cities']:
        raise MapValidationError('Map must contain a non-empty cities array.')
    if not isinstance(data.get('roads'), list):
        raise MapValidationError('Map must contain a roads array.')
    if len(data['cities']) > 1500 or len(data['roads']) > 20000:
        raise MapValidationError('Map exceeds the permitted demo size.')
    if data.get('unit', 'km') != 'km':
        raise MapValidationError('Only distances in km are supported.')
    cities, roads, names = [], [], set()
    for city in data['cities']:
        if not isinstance(city, dict):
            raise MapValidationError('Every city must be an object.')
        name, x, y = city.get('name'), city.get('x'), city.get('y')
        if not isinstance(name, str) or not name.strip() or len(name) > 80:
            raise MapValidationError('Each city needs a non-empty name (max 80 characters).')
        if name in names:
            raise MapValidationError(f'Duplicate city: {name}')
        if any(isinstance(z, bool) or not isinstance(z, (int, float)) or not math.isfinite(z) for z in (x, y)):
            raise MapValidationError(f'City {name} needs finite numeric x/y coordinates.')
        names.add(name)
        cities.append({'name': name, 'x': x, 'y': y})
    adj = {name: [] for name in names}
    edges = set()
    for road in data['roads']:
        if not isinstance(road, dict):
            raise MapValidationError('Every road must be an object.')
        a, b, km = road.get('from'), road.get('to'), road.get('km')
        if a not in names or b not in names:
            raise MapValidationError(f'Road references an unknown city: {a} / {b}')
        if a == b:
            raise MapValidationError('Self-loop roads are not supported.')
        if isinstance(km, bool) or not isinstance(km, (int, float)) or not math.isfinite(km) or km <= 0:
            raise MapValidationError('Road distances must be positive numbers.')
        key = tuple(sorted((a, b)))
        if key in edges:
            raise MapValidationError(f'Duplicate road: {a} / {b}')
        edges.add(key)
        roads.append({'from': a, 'to': b, 'km': km})
        adj[a].append((b, km))
        adj[b].append((a, km))
    for name in adj:
        adj[name].sort(key=lambda item: item[0])
    normalized = {'name': str(data.get('name') or 'Custom Map')[:100], 'unit': 'km', 'cities': cities, 'roads': roads}
    return normalized, adj


def route_cost(adj, path):
    if not path:
        return None
    total = 0
    for a, b in zip(path, path[1:]):
        matches = [cost for neighbor, cost in adj[a] if neighbor == b]
        if not matches:
            raise ValueError(f'Invalid path edge: {a} -> {b}')
        total += matches[0]
    return total
