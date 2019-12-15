import unittest
from src.worlds.grid_world import GridWorld


class TestGridWorld(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gridWorld = GridWorld()
        pass

    def test_perform_action(self):
        self.gridWorld.load_grid_from_file("grid_1.txt")
        pass

