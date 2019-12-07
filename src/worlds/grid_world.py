from abc import ABC
import numpy as np

from .abstract_world import AbstractWorld


##
# Grid World
#


class GridWorld(AbstractWorld, ABC):

    def __init__(self):
        super().__init__()

    def run_policy(self, policy, iterations=1):
        pass

    ##
    # Determines the reward and resulting state after performing an action on the given state
    #
    # Actions selected are weighted using the probabilities defined in self._state_actions.get(state, action)
    #
    # @param state The starting state
    # @param action The action to perform
    # @return the resulting state
    #
    def perform_action(self, state, action):
        reward = self._state_actions.get((state, action))[0]
        successors = [s for s in self._state_actions.get((state, action))[1]]
        probabilities, successor_states = zip(*successors)

        successor_states = np.array(successor_states, dtype=object)

        next_state = successor_states[np.random.choice(len(successor_states), p=probabilities)]
        return next_state, reward

