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
        self.grid_width = 0
        self.grid_height = 0
        self._grid = []
        self.probabilities={
            self.Action.UP: 0.8,
            self.Action.RIGHT: 0.1,
            self.Action.LEFT: 0.1,
            self.Action.DOWN: 0.0,
            self.Action.EXIT: 1.0
        }
        self.normal_reward = 1
        self.trap_exit_reward = -1
        self.goal_exit_reward = 10
        self.load_grid_from_file("grid_1.txt")
        self._initialize_mdp()

    ##
    # Check whether a state with locations (x,y) is a terminal state
    #
    # @param state an (x, y) tuple
    # @return true/false
    def is_terminal_state(self, state):
        if self._state_types[state[0]][state[1]] == "R" or self._state_types[state[0]][state[1]] == "G":
            return True
        else:
            return False

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
        next_state = None
        reward = self.reward(state, action)

        transitions = self.get_transitions(state, action)
        probabilities, successor_states = zip(*transitions)

        successor_states = np.array(successor_states, dtype=object)

        next_state = successor_states[np.random.choice(len(successor_states), p=probabilities)]
        return tuple(next_state), reward


    ##
    #
    #

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
    def load_grid_from_file(self, filename):

        directory = Path(__file__).parent / "grids"

        # Preload grid_ values
        with open(directory / filename) as file:
            lines = file.readlines()
            self.grid_width = len(lines)
            self.grid_height = len(lines[0].replace('\n',''))

            self._state_types = [None] * self.grid_height
            self._grid = [None] * self.grid_height
            for i in range(self.grid_width):

                self._state_types[i] = [None] * self.grid_width
                self._grid[i] = [None] * self.grid_width
                for j in range(self.grid_height):
                    # Store state types
                    self._state_types[i][j] = lines[i][j]
                    self._grid[i][j] = lines[i][j]

    ##
    #
    #
    #
    def _initialize_mdp(self):
        # Iterate all Possible states
        for i in range(self.grid_width):
            for j in range(self.grid_height):

                state = (i, j)

                # For Each Valid State
                if self._is_valid_grid_location(i, j):

                    # Handle Terminal States
                    if self.is_terminal_state(state):
                        if self._state_types[state[0]][state[1]] == "R":
                            self.add_transition_old(((state, self.Action.EXIT), [(self.probabilities[self.Action.EXIT], None)]))
                        elif self._state_types[state[0]][state[1]] == "G":
                            self.add_transition_old(((state, self.Action.EXIT), [(self.probabilities[self.Action.EXIT], None)]))

                    # Handle Non-Terminal States
                    else:
                        # Create list of "normal" actions (no exit action)
                        normal_actions = list(self.Action)
                        normal_actions.remove(self.Action.EXIT)

                        # For Each Normal Action (no exit action)
                        for action_choice in normal_actions:

                            transitions = []
                            # Handle Stochastic Features
                            # For Each Possible Resulting Action
                            for stocastic_action in self.RelativeAction:

                                resulting_action = self._get_relative_action(action_choice, stocastic_action)
                                resulting_state = self._get_target_state(state, resulting_action)

                                # Check if the resulting state is value
                                if self._is_valid_grid_location(resulting_state[0], resulting_state[1]):

                                    # trap case
                                    if self._grid[resulting_state[0]][resulting_state[1]] == "R":
                                        transitions.append((self.probabilities[self.Action(stocastic_action.value)], resulting_state))

                                    # goal case
                                    elif self._state_types[resulting_state[0]][resulting_state[1]] == "G":
                                        transitions.append((self.probabilities[self.Action(stocastic_action.value)], resulting_state))

                                    # Start & Normal States case
                                    else:
                                        transitions.append((self.probabilities[self.Action(stocastic_action.value)], resulting_state))

                                # If resulting state is invalid, stay in original state
                                else:
                                    transitions.append((self.probabilities[self.Action(stocastic_action.value)], state)) # Stay in same state

                            #r, t = zip(*transitions.copy())
                            #self.add_transition_old(((state, action_choice), t))
                            self.add_transition(state, action_choice, transitions)

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
    # @relative_action_ the stochastic action. Up = chosen action, Down = reverse action
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
            raise ValueError("Invalid Stochastic Action")

        return resulting_action

    def _is_valid(self, x, y):
        # if is_valid_grid_index(state, max_index_x, max_index_y):
        # return False
        # elif self._state_types[state[0]][[state[1]] == "B":
        # return False
        # else:
        # return True
        pass

    ##
    # Checks if a location (x, y) is a valid location
    #
    # @param x the x coordinate
    # @param y the y coordinate
    # @return true/false
    def _is_valid_grid_location(self, x, y):
        return self._is_valid_grid_coordinate(x, y) and self._grid[x][y] != "B"

    ##
    # Checks if a location (x, y) is in the grid space
    #
    # @param x the x coordinate
    # @param y the y coordinate
    # @return true/false
    def _is_valid_grid_coordinate(self, x, y):
        if x < 0 or x > self.grid_width - 1 or \
           y < 0 or y > self.grid_height - 1:
            return False
        else:
            return True

    ##
    # Inner Enumeration class representing the 4 stocastic action choices
    #
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
        EXIT = 4

    ##
    # Reward Function
    #
    #
    def reward(self, state, action):
        if self._state_types[state[0]][state[1]] == "W":
            return self.normal_reward
        elif self._state_types[state[0]][state[1]] == "R":
            return self.trap_exit_reward
        elif self._state_types[state[0]][state[1]] == "G":
            return self.goal_exit_reward
        elif self._state_types[state[0]][state[1]] == "Y":
            return self.normal_reward
        else:
            raise ValueError
