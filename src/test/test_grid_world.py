import unittest
from src.worlds.grid_world import GridWorld


class TestGridWorld(unittest.TestCase):

    def __init__(self):
        self.gridWorld = GridWorld()
        pass

    def test_relative(self):
        self.gridWorld.load_grid_from_file("grid_1.txt")
        pass

