from interface import implements
from .policy_algorithm import PolicyAlgorithm
from worlds.abstract_world import AbstractWorld
import random

##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#


class MontyCarlo(implements(PolicyAlgorithm)):

    def __init__(self):
        pass

    def generate_policy(self, world):

        states = world.get_states()
        policy = {}
        q_values = {}

        # Initialization
        for state in states:
            possible_actions = world.get_actions(state)
            policy[state] = random.choice(possible_actions)

            for action in possible_actions:
                q_values[(state, action)] = 0.0


        # Loop

            start_state = random.choice(states)

        print("sdads")
        pass
