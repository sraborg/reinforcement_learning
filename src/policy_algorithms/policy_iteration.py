from interface import implements
from .policy_algorithm import PolicyAlgorithm
from .policy_analytics.default_policy_analytics import DefaultPolicyAnalytics
import random
from operator import itemgetter


##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#

class PolicyIteration(implements(PolicyAlgorithm)):

    def __init__(self):
        super().__init__()
        self._world = None
        self._policy_table = None
        self._gamma = .9
        self._value_table = None
        self.evaluations = 0
        self._policy_stable = True
        self._policy_improvement_analytics = DefaultPolicyAnalytics()
        self._policy_evaluation_analytics = DefaultPolicyAnalytics()
        self.evaluation_improvement_cycles = 0

    ##
    # Generates a policy
    #
    # @param world the domain to learn a policy for
    def generate_policy(self, world):
        self._policy_evaluation_analytics.reset()
        self._policy_improvement_analytics.reset()

        # Initialize
        self._world = world
        self._value_table = {}
        self._policy_table = {}
        for state in world.get_states():
            self._value_table[state] = 0.0
            self._policy_table[state] = random.choice(world.get_actions(state))

        i = 0
        self.evaluation_improvement_cycles = 0
        while(True):
            self.policy_evalation()
            self.policy_improvement()
            i += 1
            if(self._policy_stable):
                break

        print("Policy Evaluation/Improvement Cycles: " + str(self.evaluation_improvement_cycles))
        print(self._policy_improvement_analytics.get_analytics())
        print(self._policy_evaluation_analytics.get_analytics())
        return self._policy_table.copy()

    ##
    # Evaluates the self._policy_table
    #
    # Uses Standard policy Evaluation Algorithm
    #
    def policy_evalation(self, iterations=10000, theta=.5):
        delta = 0

        for i in range(iterations):

            for state in self._world.get_states():
                self._policy_evaluation_analytics.increment_states_searched()

                old_value = self._value_table[state]       # Current value
                action = self._policy_table[state]

                transitions = self._world.get_transitions(state, action)

                temp_rewards = []
                for probability, next_state in transitions:
                    self._policy_evaluation_analytics.increment_states_searched()
                    reward = self._world.reward(state, action)

                    # Check for Exit Action Case
                    if next_state is None:
                        temp_rewards.append(reward)
                    else:
                        temp_rewards.append(probability * (reward + self._gamma * self._value_table[next_state]))

                self._value_table[state] = max(temp_rewards)
                delta = max(delta, abs(old_value - self._value_table[state]))

            # Test for early convergence
            if (delta < theta):
                self._policy_evaluation_analytics.set_convergence_iteration(i)
                break

    ##
    # Improves a current policy
    #
    # Uses standard Policy Improvement Algorithm
    #
    def policy_improvement(self):
        self._policy_stable = True

        for state in self._world.get_states():

            self._policy_improvement_analytics.increment_states_searched()
            old_action = self._policy_table[state]

            actions_values = []
            for action in self._world.get_actions(state):
                self._policy_improvement_analytics.increment_action_searched()
                transitions = self._world.get_transitions(state, action)

                temp_rewards = []
                for probability, next_state in transitions:
                    self._policy_improvement_analytics.increment_states_searched()

                    # Check for Exit Case
                    if next_state is None:
                        temp_rewards.append(self._world.reward(state, action))
                    else:
                        temp_rewards.append(probability * (self._world.reward(state, action) + self._gamma * self._value_table[next_state]))

                actions_values.append((action, max(temp_rewards)))

            new_action = max(actions_values, key=itemgetter(1))[0]
            self._policy_table[state] = new_action

            if self._policy_table[state] is not old_action:
                self._policy_stable = False

        if not self._policy_stable:
            self.policy_evalation()
