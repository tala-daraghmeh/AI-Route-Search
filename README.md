# 🗺️ AI Route Search · ROUTELAB

**An interactive route-finding web application powered by AI search algorithms.**

A Flask-based web application developed for the *Fundamentals of Artificial Intelligence* course at An-Najah National University.

ROUTELAB explores how different search strategies navigate a road network. Users can choose cities, run algorithms, visualize routes, compare results, and upload custom maps.

---

## 👥 Team Members

| Name | Student ID |
|---|---|
| Tala Daraghmeh | 12429337 |
| Yazan Nasser | 12400750 |
| Bahaa Alshami | 12428749 |

---

## 🚀 Get Started

**Requirements:** Python 3.10+

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/tala-daraghmeh/AI-Route-Search.git
cd AI-Route-Search
```

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies and run the application:

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000/** in your browser.

---

## 🧠 Search Algorithms

ROUTELAB implements five search strategies covered in the AI course.

| Algorithm | Search Type | Main Idea |
|---|---|---|
| BFS | Uninformed | Explores nodes level by level |
| DFS | Uninformed | Explores one branch deeply before backtracking |
| UCS | Uninformed | Expands the node with the lowest path cost |
| Greedy Best-First | Informed | Uses a heuristic to guide the search |
| A* | Informed | Combines path cost and heuristic estimates |

### ⚙️ Team Algorithm Contract

Every search algorithm follows the same interface:

```python
def search(graph, start, goal):
    return {
        "path": [...],
        "cost": ...,
        "steps": ...
    }
```

**Implementation rules:**

- `graph` contains cities and their weighted road connections.
- `start` and `goal` represent the selected cities.
- `path` contains the ordered cities along the discovered route.
- `cost` is the sum of road distances in kilometers.
- `steps` counts expanded nodes according to the assignment rules.
- If no route exists, return an empty path and `None` cost.
- If start equals goal, return the single-city path with cost 0.
- Goal testing occurs when a node is removed from the frontier.
- Each city is expanded at most once.
- Alphabetical tie-breaking is applied where required.

All five algorithms are implemented manually without ready-made search or graph libraries.

---

## ✨ Features

### 🗺️ Interactive Network Visualization

Displays cities and weighted roads using a graphical network visualization.

- Shows road connections and distance labels.
- Highlights the route returned by the selected algorithm.
- Distinguishes the start and goal cities.

### 🔎 Route Search

Users can select:

- Start city
- Goal city
- Search algorithm

The application displays the resulting path, total distance (km), and number of expanded nodes.

### 📊 Compare All

Runs all five search algorithms and displays their results side by side.

The comparison includes:

- Algorithm name
- Selected route
- Total path cost
- Expansion steps

Users can select a comparison result to view its route on the map.

### 📂 Custom JSON Map Upload

Supports uploading a different road network as a JSON file.

The uploaded map is validated before use. Users can also restore the default map.

---

## 🌐 API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/` | GET | Web interface |
| `/api/map` | GET | Read active map |
| `/api/map` | POST multipart `file` | Upload and validate JSON map |
| `/api/map/reset` | POST | Restore default West Bank map |
| `/api/search` | POST JSON | Run one algorithm |
| `/api/compare` | POST JSON | Run all five algorithms |

**Example request for `/api/search`:**

```json
{
  "start": "Jenin",
  "goal": "Hebron",
  "algorithm": "bfs"
}
```

The selected map is stored server-side for the browser session while the development server is running. Uploaded maps are not saved permanently.

The Flask development server is intended for local testing and demonstration.

---

## 📁 Project Structure

```text
AI-Route-Search/
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── ucs.py
│   ├── greedy.py
│   └── astar.py
│
├── data/
│   └── westbank_map.json
│
├── static/
│   ├── style.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── tests/
├── utils/
├── app.py
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

The automated tests cover graph validation, bidirectional roads, deterministic neighbor ordering, and known route costs.

The team also performed manual integration testing of the five algorithms, including:

- Route and path-cost calculations
- Expanded-node counts
- Start and goal being the same city
- Unreachable destinations
- Compare All results
- Route visualization

---

## 📍 Default Road Network

The default dataset is stored in:

`data/westbank_map.json`

It contains **11 West Bank cities and 19 bidirectional roads**, with distances measured in kilometers.

The application uses this network to demonstrate and compare the behavior of different AI search strategies.

---

## 🎓 Official Assignment

**University:** An-Najah National University  
**Course:** Fundamentals of Artificial Intelligence  
**Assignment:** Assignment 1 · Route Search Web Application  
**Instructor:** Nadeem Zaid Kilani

**Project requirements:**

- Implement BFS, DFS, UCS, Greedy Best-First, and A*.
- Find routes between any two cities in the provided network.
- Display the path, distance, and expanded-node count.
- Visualize the network and highlight selected routes.
- Compare all algorithms.
- Support uploading new road maps in JSON format.

---

**ROUTELAB | Exploring paths, comparing strategies, understanding search.**
