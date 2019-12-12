from interface import implements
from .policy_algorithm import PolicyAlgorithm
from worlds.abstract_world import AbstractWorld
from statistics import mean
import random

##
# Policy Iteration Algorithm
#
# Uses policy iteration to generate policies
#


class MontyCarlo(implements(PolicyAlgorithm)):

    def __init__(self):
        super().__init__()
        self._world = None
        self._policy_table = None
        self._gamma = .9
        self.evaluations = 0
        self._value_table = None
        self._returns = None

    def generate_policy(self, world):
        self._world = world
        states = world.get_states()
        self._policy_table = {}
        self._value_table = {}
        self._returns = {}

        # Initialization
        for state in states:
            self._returns[state] = []
            possible_actions = world.get_actions(state)
            self._policy_table[state] = random.choice(world.get_actions(state))

        self._approximate_values()
        self._extract_policy()
        return self._policy_table.copy()

    ##
    # Implements Monte Carlo Learning Loop
    #
    def _approximate_values(self, iterations=1000):

        for i in range(iterations):
            states = self._world.get_states()
            start_state = random.choice(states)  # Random Start State
            episode = self.generate_episode(self._world, self._policy_table, start_state)
            G = 0
            reversed_episode = episode[::-1]

            for j, step in enumerate(reversed_episode, start=1):
                state = step[0]
                prior_step_reward = reversed_episode[j - 1][2]  # prior known reward

                G = self._gamma * G + prior_step_reward

                # Make Sure this state doesn't appear further in the list (e.g. at an earlier time in the episode)
                if not [s for s in reversed_episode[j + 1::] if s[0] == step[0] and s[1] == step[1]]:
                    self._returns[state].append(G)
                    self._value_table[state] = mean(self._returns[state])

    def generate_episode(self, world, policy, start_state):
        episode = []
        next_state = start_state

        i = 0
        while not world.is_terminal_state(next_state):
            state = next_state
            action = policy[next_state]
            next_state, reward = world.perform_action(next_state, action)  # Perform Step

            episode.append((state, policy[next_state], reward, next_state))         # Add (state, action, reward) to episode

            i = i +1

        return episode

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
                                    self._world.reward(state, action) + self.gamma * self._value_table[next_state]))

                actions_values.append((action, max(temp_rewards)))

            #self.state_complexity = self.state_complexity + 1
            #self.action_complexity = self.action_complexity + 1

            new_action = max(actions_values, key=itemgetter(1))[0]
            self._policy_table[state] = new_action