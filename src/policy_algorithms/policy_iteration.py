from interface import implements
from .policy_algorithm import PolicyAlgorithm
import numpy as np


##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#


class PolicyIteration(implements(PolicyAlgorithm)):
    max_iterations = 1000

    def generate_policy(self, world):
        # mdp = world._state_actions

        value_table = {}
        for state in world.get_states():
            value_table[state] = 0.0

        print(value_table[(1, 1)])

        z, x = world.perform_action((1, 1), world.Action.DOWN)
        print(z)
        print(x)

        evaluated_policies = 1
        # for i in range(int(self.max_iterations)):
        #    stable_policy = True
        #    V = policy_evaluation(policy, environment, discount_factor=discount_factor)
