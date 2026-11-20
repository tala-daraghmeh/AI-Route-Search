# AI Route Search · ROUTELAB

A Flask-based web UI for the *Fundamentals of Artificial Intelligence* route-search assignment. The interface includes a network visualizer, JSON map upload, search controls, and Compare All table. **The five search algorithms are placeholders by design:** students implement BFS, DFS, UCS, Greedy Best-First, and A* themselves.

## Get started

Install Python 3.10+ and open this folder in VS Code.

```bash
python -m venv .venv
```

Activate your virtual environment on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install and run:

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000/**.

## Team algorithm contract

Your team should agree on this shared contract before implementing the algorithms:

```python
# algorithms/bfs.py  (same for dfs.py, ucs.py, greedy.py, astar.py)
def search(graph, start, goal):
    # graph: dict[str, list[tuple[str, number]]]
    # start, goal: city name strings
    return {"path": [start, "...", goal], "cost": 123, "steps": 5}
```

The example above is just a shape, **not valid output to copy**. In an actual implementation:

- `path` includes the start and goal, with each consecutive city pair connected by a road.
- `cost` is the sum of road weights along the path. The backend checks this.
- `steps` is an integer counting expanded nodes per assignment rules.
- For no available route, return `{"path": [], "cost": None, "steps": number_of_expanded_nodes}`.
- For start == goal, return a single-city path with cost 0 and correct expanded step count.
- Goal test must happen on frontier removal; never expand the same city twice; alphabetical tie-breaking.
- Implement BFS/DFS/UCS/Greedy/A* manually. Do not use ready-made search/graph libraries.

Each algorithm currently raises `NotImplementedError` until your team replaces the function. The UI shows an explicit *not implemented* message, not fake search results.

## API endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Web interface |
| `/api/map` | GET | Read active map |
| `/api/map` | POST multipart `file` | Upload and validate JSON map |
| `/api/map/reset` | POST | Restore default West Bank map |
| `/api/search` | POST JSON | Run one algorithm |
| `/api/compare` | POST JSON | Run all five and compare |

Example JSON request for `/api/search`:

```json
{"start":"Jenin","goal":"Hebron","algorithm":"bfs"}
```

The selected JSON map is stored server-side for each browser session while the development server is running. Uploaded maps are not saved permanently. In production, implement persistent storage and a secure secret key. `app.run(debug=True)` is for local development only.

## Integrating with existing repo

This is an independent frontend/backend scaffold based on the assignment JSON. The actual existing GitHub contents were not available for automatic merge in this session. **Do not overwrite teammates' implementations.** Inspect diffs and copy only needed files, then commit in a new branch.

Recommended branch: `feature/flask-interface`. If algorithm files exist and already contain real implementations, keep those versions and only ensure each exports the agreed `search(graph, start, goal)` function. Similarly review your current README before replacing it.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover map validation, bidirectional roads, deterministic neighbor ordering, and known route cost. End-to-end tests for algorithm correctness need to be added by the team.

## Official assignment

Default map: 11 cities and 19 bidirectional roads in `data/westbank_map.json`. All five algorithms must return route, km and expansion count. The UI must draw the network, display highlighted paths, support uploading map JSON, compare results, and identify the lowest cost. Every team member must understand the complete code for the discussion.
