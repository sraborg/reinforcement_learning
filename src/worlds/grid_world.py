from abc import ABC

from .abstract_world import AbstractWorld


##
# Grid World
#


class GridWorld(AbstractWorld, ABC):

    def __init__(self):
        super().__init__()

    def run_policy(self, policy, iterations=1):
        pass

    def perform_action(self, state, action):
        pass
