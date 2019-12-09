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
    discount_factor = 1.0

    def policy_evaluation(self, value_table, world):
        return 0

    def lookahead(self, world, state, val_v):
        return 0

    def generate_policy(self, world):
        # mdp = world._state_actions
        num_runs = 0
        value_table = {}
        for state, action in world.get_states():
            value_table[state] = action

        for i in range(self.max_iterations):
            is_stable = False
            # val_v = self.policy_evaluation(value_table, world)

            # for state in world.get_states():
            # print(world.get_actions(state))
            break

        print(value_table)
        """
                current_action = np.argmax(state.get_actions())
                action_value = self.lookahead(world, state, val_v)
                best_action = np.argmax(action_value)

                if current_action != best_action:

        z, x = world.perform_action((2, 6), world.Action.RIGHT)
        print(z)
        print(x)
        """
        evaluated_policies = 1
        # for i in range(int(self.max_iterations)):
        #    stable_policy = True
        #    V = policy_evaluation(policy, environment, discount_factor=discount_factor)
