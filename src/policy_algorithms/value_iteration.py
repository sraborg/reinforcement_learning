from interface import implements
from .policy_algorithm import PolicyAlgorithm
from operator import itemgetter

##
# Value Iteration Algorithm
#
# Uses value iteration to generate policies
#


class ValueIteration(implements(PolicyAlgorithm)):

    def __init__(self):
        super().__init__()
        self._world = None
        self._policy_table = None
        self._gamma = .9
        self._value_table = None
        self.evaluations = 0
        self._policy_stable = True

    def generate_policy(self, world):
        # Initialize
        self._world = world
        self._value_table = {}
        self._policy_table = {}
        for state in world.get_states():
            if self._world.is_terminal_state(state):
                self._value_table[state] = 0
            else:
                self._value_table[state] = 0.0

        self._value_iteration()
        self._extract_policy()
        return self._policy_table.copy()

    def _value_iteration(self, iterations=1000, theta=.5):

        for i in range(iterations):
            delta = 0
            for state in self._world.get_states():
                old_value = self._value_table[state]

                for action in self._world.get_actions(state):

                    transitions = self._world.get_transitions(state, action)

                    temp_rewards = []
                    for probability, next_state in transitions:

                        reward = self._world.reward(state, action)

                        # Check for Exit Action Case
                        if next_state is None:
                            temp_rewards.append(reward)
                        else:
                            temp_rewards.append(probability * (reward + self._gamma * self._value_table[next_state]))

                    self._value_table[state] = max(temp_rewards)
                    delta = max(delta, abs(old_value - self._value_table[state]))

            # Test for early convergence
            if delta < theta:
                break


    def _extract_policy(self):

        for state in self._world.get_states():

            actions_values = []
            for action in self._world.get_actions(state):
                #self.action_complexity = self.action_complexity + 1
                transitions = self._world.get_transitions(state, action)

                temp_rewards = []
                for probability, next_state in transitions:

                    # Check for Exit Case
                    if next_state is None:
                        temp_rewards.append(self._world.reward(state, action))
                    else:
                        temp_rewards.append(probability * (
                                    self._world.reward(state, action) + self._gamma * self._value_table[next_state]))

                actions_values.append((action, max(temp_rewards)))

            #self.state_complexity = self.state_complexity + 1
            #self.action_complexity = self.action_complexity + 1

            new_action = max(actions_values, key=itemgetter(1))[0]
            self._policy_table[state] = new_action

