from interface import implements
from .policy_algorithm import PolicyAlgorithm
import random
import numpy as np


##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#


class PolicyIteration(implements(PolicyAlgorithm)):

    def __init__(self):
        self._world = None
        self._values_table = None
        self._policy_table = None
    def policy_evaluation(self, value_table, world):
        return 0

    def generate_policy(self, world):

        # Initialize
        self._world = world
        self._value_table = {}
        self._policy_table = {}
        for state in world.get_states():
            self._value_table[state] = 0.0
            self._policy_table[state] = random.choice(world.get_actions(state))

        self.policy_evalution()

    def policy_evalution(self, iterations=1000, theta=.5):
        delta = 0

        for state in self._world.get_states():
            v = self._policy_table[state]       # Current value

            transitions = self._world.get_transitions(state, self._policy_table[state])
            #for action in transitions:


        pass
