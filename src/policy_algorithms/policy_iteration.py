from interface import implements
from .policy_algorithm import PolicyAlgorithm
from .policy_analytics import PolicyAnalytics
import random
from operator import itemgetter


##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#

class PolicyIteration(PolicyAnalytics, implements(PolicyAlgorithm)):

    def __init__(self):
        super().__init__()
        self._world = None
        self._value_table = None
        self._policy_table = None
        self.evaluations = 0
        self.gamma = .9
        self._policy_stable = True

    ##
    # Generates a policy
    #
    # @param world the domain to learn a policy for
    def generate_policy(self, world):

        # Initialize
        self._world = world
        self._value_table = {}
        self._policy_table = {}
        for state in world.get_states():
            self._value_table[state] = 0.0
            self._policy_table[state] = random.choice(world.get_actions(state))


        while(True):
            self.policy_evalation()
            self.policy_improvement()
            if(self._policy_stable):
                break

        return self._policy_table.copy()

    ##
    # Evaluates the self._policy_table
    #
    # Uses Standard policy Evaluation Algorithm
    #
    def policy_evalation(self, iterations=1000, theta=.5):
        delta = 0

        for i in range(iterations):
            #self.state_complexity = self.state_complexity + 1

            for state in self._world.get_states():
                self.states_searched = self.states_searched + 1
                old_value = self._value_table[state]       # Current value

                transitions = self._world.get_transitions(state, self._policy_table[state])

                temp_rewards = []
                for probability, next_state, reward in transitions:

                    # Check for Exit Case
                    if next_state is None:
                        temp_rewards.append(reward)
                    else:
                        temp_rewards.append(probability * (reward + self.gamma * self._value_table[next_state]))

                self._value_table[state] = sum(temp_rewards)
                delta = max(delta, abs(old_value - self._value_table[state]))

            # Test for early convergence
            if (delta < theta):
                break

    ##
    # Improves a current policy
    #
    # Uses standard Policy Improvement Algorithm
    #
    def policy_improvement(self):
        self._policy_stable = True

        for state in self._world.get_states():
            self.state_complexity = self.state_complexity + 1
            old_action = self._policy_table[state]

            actions_values = []
            for action in self._world.get_actions(state):
                self.action_complexity = self.action_complexity + 1
                transitions = self._world.get_transitions(state, action)

                temp_rewards = []
                for probability, next_state, reward in transitions:

                    # Check for Exit Case
                    if next_state is None:
                        temp_rewards.append(reward)
                    else:
                        temp_rewards.append(probability * (reward + self.gamma * self._value_table[next_state]))

                actions_values.append((action, max(temp_rewards)))

            self.state_complexity = self.state_complexity + 1
            self.action_complexity = self.action_complexity + 1

            new_action = max(actions_values, key=itemgetter(1))[0]
            self._policy_table[state] = new_action

            if self._policy_table[state] is not old_action:
                self._policy_stable = False

        if not self._policy_stable:
            self.policy_evalation()
