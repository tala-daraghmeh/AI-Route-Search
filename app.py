"""Flask API + UI for AI Route Search. Search logic lives in algorithms/*.py."""
import importlib
import json
import os
from pathlib import Path
from uuid import uuid4
from flask import Flask, jsonify, render_template, request, session
from utils.graph import prepare_map, MapValidationError, route_cost

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY') or os.urandom(32)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
ALGORITHMS = {'bfs': 'BFS', 'dfs': 'DFS', 'ucs': 'UCS', 'greedy': 'Greedy Best-First', 'astar': 'A*'}
CUSTOM_MAPS = {}  # Session-isolated in-memory uploads; cleared on restart.
with (ROOT / 'data' / 'westbank_map.json').open(encoding='utf-8') as f:
    DEFAULT_MAP, _ = prepare_map(json.load(f))


def active_map():
    map_id = session.get('map_id')
    return CUSTOM_MAPS.get(map_id, DEFAULT_MAP)


def error(message, status=400):
    return jsonify({'error': message}), status


def run_search(key, graph, start, goal):
    module = importlib.import_module(f'algorithms.{key}')
    try:
        result = module.search(graph, start, goal)
    except NotImplementedError:
        return {'algorithm': key, 'status': 'not_implemented', 'message': f'{ALGORITHMS[key]} has not been implemented by the team yet.'}
    if not isinstance(result, dict):
        raise ValueError('Algorithm must return a result dictionary.')
    path, steps = result.get('path'), result.get('steps')
    if not isinstance(path, list) or not all(isinstance(x, str) for x in path):
        raise ValueError('Algorithm result must include a path list.')
    if not isinstance(steps, int) or isinstance(steps, bool) or steps < 0:
        raise ValueError('Algorithm result must include nonnegative integer steps.')
    if path and (path[0] != start or path[-1] != goal):
        raise ValueError('Path must start at the start city and end at the goal city.')
    if any(city not in graph for city in path):
        raise ValueError('Path includes a city not in the map.')
    cost = route_cost(graph, path)
    reported_cost = result.get('cost')
    if reported_cost != cost:
        raise ValueError(f'Algorithm returned incorrect cost (expected {cost}, got {reported_cost}).')
    return {'algorithm': key, 'status': 'ok' if path else 'no_path', 'path': path, 'cost': cost, 'steps': steps}


def search_inputs():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        raise ValueError('Send a JSON object with start and goal.')
    map_data, graph = prepare_map(active_map())
    start, goal = payload.get('start'), payload.get('goal')
    if start not in graph or goal not in graph:
        raise ValueError('Choose a valid starting city and destination.')
    return payload, graph, start, goal


@app.get('/')
def home():
    return render_template('index.html')


@app.get('/api/map')
def get_map():
    return jsonify(active_map())


@app.post('/api/map')
def upload_map():
    try:
        if 'file' not in request.files:
            return error('Choose a JSON file to upload.')
        file = request.files['file']
        if not file.filename.lower().endswith('.json'):
            return error('Only .json files are supported.')
        contents = json.load(file.stream)
        data, _ = prepare_map(contents)
    except (ValueError, UnicodeError, json.JSONDecodeError, MapValidationError) as exc:
        return error(f'Invalid map: {exc}')
    old_id = session.get('map_id')
    if old_id:
        CUSTOM_MAPS.pop(old_id, None)
    map_id = uuid4().hex
    CUSTOM_MAPS[map_id] = data
    session['map_id'] = map_id
    return jsonify(data)


@app.post('/api/map/reset')
def reset_map():
    old_id = session.pop('map_id', None)
    if old_id:
        CUSTOM_MAPS.pop(old_id, None)
    return jsonify(DEFAULT_MAP)


@app.post('/api/search')
def search():
    try:
        payload, graph, start, goal = search_inputs()
        key = payload.get('algorithm')
        if key not in ALGORITHMS:
            return error('Choose a valid algorithm.')
        return jsonify(run_search(key, graph, start, goal))
    except ValueError as exc:
        return error(str(exc))
    except Exception:
        app.logger.exception('Algorithm failed')
        return error('Algorithm failed during execution. Check the terminal logs.', 500)


@app.post('/api/compare')
def compare():
    try:
        _, graph, start, goal = search_inputs()
        results = []
        for key in ALGORITHMS:
            try:
                results.append(run_search(key, graph, start, goal))
            except Exception as exc:
                app.logger.exception('Algorithm %s failed', key)
                results.append({'algorithm': key, 'status': 'error', 'message': str(exc)})
        costs = [r['cost'] for r in results if r['status'] == 'ok']
        best = min(costs) if costs else None
        for result in results:
            result['optimal'] = result['status'] == 'ok' and result['cost'] == best
        return jsonify({'results': results, 'minimum_found_cost': best, 'all_implemented': all(r['status'] not in ('not_implemented', 'error') for r in results)})
    except ValueError as exc:
        return error(str(exc))


@app.get('/api/status')
def status():
    return jsonify({'algorithms': list(ALGORITHMS), 'map': active_map()['name']})


@app.errorhandler(413)
def too_large(_):
    return error('File is too large (maximum 2 MB).', 413)


if __name__ == '__main__':
    app.run(debug=True)
