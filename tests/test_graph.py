import json
import unittest
from pathlib import Path
from utils.graph import prepare_map, route_cost, MapValidationError

ROOT = Path(__file__).resolve().parents[1]

class GraphTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'data'/'westbank_map.json').read_text())
        self.map, self.graph = prepare_map(self.data)

    def test_default_map(self):
        self.assertEqual(len(self.map['cities']), 11)
        self.assertEqual(len(self.map['roads']), 19)

    def test_undirected_and_sorted(self):
        for city, neighbors in self.graph.items():
            self.assertEqual([n for n,_ in neighbors], sorted(n for n,_ in neighbors))
            for neighbor, km in neighbors:
                self.assertIn((city, km), self.graph[neighbor])

    def test_known_route_cost(self):
        self.assertEqual(route_cost(self.graph, ['Jenin','Nablus','Ramallah']), 90)

    def test_duplicate_city_rejected(self):
        self.data['cities'].append(self.data['cities'][0])
        with self.assertRaises(MapValidationError):
            prepare_map(self.data)

if __name__=='__main__':
    unittest.main()
