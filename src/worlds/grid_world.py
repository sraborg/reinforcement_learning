from abc import ABC
from pathlib import Path
from enum import Enum
import numpy as np

from .abstract_world import AbstractWorld


##
# Grid World
#


class GridWorld(AbstractWorld, ABC):

    ##
    # Constructor
    #
    def __init__(self):
        super().__init__()
        self.load_grid_from_file("grid_1.txt")
        self.perform_action((1,0), self.Action.RIGHT)
        print(self.get_states())

    ##
    # Generates episodes using a given policy
    #
    # @param the policy to follow
    # @param start_state the initial state
    # @param iterations optional keyword that determines the number of episodes to run
    #
    def run_policy(self, policy, start_state, iterations=1):
        pass
    ##
    # Determines the reward and resulting state after performing an action on the given state
    #
    # Actions selected are weighted using the probabilities defined in self._state_actions.get(state, action)
    #
    # @param state The starting state
    # @param action The action to perform
    # @return the resulting state, the reward
    #
    def perform_action(self, state, action):
        reward = self._state_actions.get((state, action))[0]
        successors = [s for s in self._state_actions.get((state, action))[1]]
        probabilities, successor_states = zip(*successors)

        successor_states = np.array(successor_states, dtype=object)

        next_state = successor_states[np.random.choice(len(successor_states), p=probabilities)]
        return tuple(next_state), reward

    ##
    # Creates an entire gridworld model by loading a file.
    #
    # File must contain a grid of x,y rows and columns. Each entry must be 'B', 'G', 'R', 'W', 'Y' where 'B' => black (invalid) state, 'G' => green (goal) state, 'R' => red (trap) state, 'W' => white (normal) state, 'Y' => yellow (start) state.
    #
    # @param filename the name of the file (e.g. grid.txt)
    # @param reward optional keyword that sets reward for white (normal) states globally
    # @param trap_value optional keyword that sets reward for red (trap) states globally
    # @param goal_value optional keyword that sets reward for green (goal) states globally
    # @param probabilities optional keyword that holds a dictionary with the following values: self.Action.UP => probability of going forward, self.Action.RIGHT => probability of going right, self.Action.LEFT => probability of going left, self.Action.DOWN => probability of going backward
    #
    def load_grid_from_file(self, filename, *,
                            reward=1,
                            trap_value=-1,
                            goal_value=10,
                            probabilities=None
                            ):

        if probabilities is None:
            probabilities={
                self.Action.UP: 0.8,
                self.Action.RIGHT: 0.1,
                self.Action.LEFT: 0.1,
                self.Action.DOWN: 0.0
            }

        ##
        # Inner Function that determines whether a (x,y) state is a valid location.
        #
        # Validates the (x,y) coordinate against the loaded file. If it valid, it also determines its states "type"
        #
        # @param x state's x coordinate
        # @param y state's y coordinate
        # @param max_index_x the number of columns
        # @param max_index_y the number of rows
        # @return boolean, type where boolean is true/false depending on if state (x,y) is valid and type is in {'B', 'G', 'R', 'W', 'Y'}
        def is_valid(state, max_index_x, max_index_y):

            # Check if in range
            if state[0] < 0 or state[0] > max_index_x - 1 or \
               state[1] < 0 or state[1] > max_index_y - 1:
                return False, None

            c = (lines[state[0]])[state[1]]

            if c == "B":
                return False, "B"
            elif c == "G":
                return True, "C"
            elif c == "Y":
                return True, "Y"
            elif c == "R":
                return True, "R"
            else:
                return True, "W"

        directory = Path("./grids")

        with open(directory / filename) as file:
            lines = file.readlines()
            MAX_INDEX_X = len(lines)
            MAX_INDEX_Y = len(lines[0].replace('\n',''))

            for i in range(MAX_INDEX_X):
                for j in range(MAX_INDEX_Y):

                    state = (i, j)

                    valid_actions_with_probabilities = []              # (probability, action)

                    # For Each Valid State
                    if is_valid(state, MAX_INDEX_X, MAX_INDEX_Y):
                        valid_actions_with_probabilities.clear()

                        # For Each Action
                        for action_choice in self.Action:
                            x,y = self._get_target_state(state, action_choice)
                            target_state = (x,y)

                            if is_valid(target_state, MAX_INDEX_X, MAX_INDEX_Y):
                                transitions = []
                                type = "W"
                                # For Each Stocastic Resulting Action
                                for stocastic_action in self.RelativeAction:

                                    resulting_action = self._get_relative_action(action_choice, stocastic_action)
                                    resulting_state = self._get_target_state(state, resulting_action)

                                    valid, type = is_valid(resulting_state, MAX_INDEX_X, MAX_INDEX_Y)
                                    if valid:
                                        if type == "R": # trap
                                            transitions.append((trap_value, (probabilities[self.Action(stocastic_action.value)], resulting_state)))
                                        elif type == "G": # trap
                                            transitions.append((goal_value, (probabilities[self.Action(stocastic_action.value)], resulting_state)))
                                        else: # Start & Normal States
                                            transitions.append((reward, (probabilities[self.Action(stocastic_action.value)], resulting_state)))
                                    else:
                                        transitions.append((reward, (probabilities[self.Action(stocastic_action.value)], state))) # Stay in same state

                                r, t = zip(*transitions.copy())
                                self.add_transition(((state, action_choice), (r[0], t)))

    ##
    # Finds the state that the provided action is trying to go to
    #
    # @param state the starting state
    # @param action_ the action to perform from the provided state
    # @return the state the action is attempting to reach
    #
    def _get_target_state(self, state, action_):
        x = state[0]
        y = state[1]

        if action_ == self.Action.RIGHT:
            y = state[1] + 1
        elif action_ == self.Action.DOWN:
            x = state[0] + 1
        elif action_ == self.Action.LEFT:
            y = state[1] - 1
        elif action_ == self.Action.UP:
            x = state[0] - 1
        else:
            raise ValueError("Invalid Action: ")

        return x, y

    ##
    # @param action_ the chosen action
    # @relative_action_ the stocastic action. Up = chosen action, Down = reverse action
    #
    # @return the result "absolute" action
    def _get_relative_action(self, action_, relative_action_):

        # Verify action
        if type(action_) is not self.Action:
            raise ValueError("Invalid Action")

        resulting_action = None

        if relative_action_.value == self.RelativeAction.FORWARD.value:  # Go Forward
            resulting_action = action_
        elif relative_action_.value == self.RelativeAction.BACKWARDS.value:  # Reverse Case
            resulting_action = self.Action((action_.value - 2) % 4)
        elif relative_action_.value == self.RelativeAction.RIGHT.value:
            resulting_action = self.Action((action_.value + 1) % 4)
        elif relative_action_.value == self.RelativeAction.LEFT.value:
            resulting_action = self.Action((action_.value - 1) % 4)
        else:
            raise ValueError("Invalid Stocastic Action")

        return resulting_action

    class RelativeAction(Enum):
        RIGHT = 0
        BACKWARDS = 1
        LEFT = 2
        FORWARD = 3

    ##
    # Inner Enumeration class representing the 4 valid grid actions
    #
    class Action(Enum):
        RIGHT = 0
        DOWN = 1
        LEFT = 2
        UP = 3




