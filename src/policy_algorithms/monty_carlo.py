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
        policy = {None: None}
        q_values = {}
        returns = {}
        # Initialization
        for state in states:
            possible_actions = world.get_actions(state)
            policy[state] = random.choice(possible_actions)

            for action in possible_actions:
                q_values[(state, action)] = 0.0


        # Infinite Loop
        while(True):
            start_state = random.choice(states)                             # Random Start State
            episode = self.generate_episode(world, policy, start_state)
            G = {}
            reversed_episode = reversed(episode)
            for i, step in enumerate(reversed_episode):
                pass

        print("sdads")
        pass

    def generate_episode(self, world, policy, start_state):
        episode = []
        state = start_state
        next_state = start_state

        i =0
        while(not world.is_terminal_state(state)):
            action = policy[next_state]
            next_state, reward = world.perform_action(next_state, action)  # Perform Step

            episode.append((state, policy[next_state], reward, next_state))         # Add (state, action, reward) to episode

            if (id(state) == id(next_state)):
                print(str(i) + "match")
                print(str(id(state)) + " ? " + str(id(next_state)))
            i = i +1

        return episode

