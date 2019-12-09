import abc

##
# Abstract Class for all worlds
#


class AbstractWorld(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        self._states = []
        self._state_actions = {}
        self._state_types = []

    @property
    def states(self):
        raise NotImplementedError

    @property
    def transitions(self, state, action):
        raise NotImplementedError

    @abc.abstractmethod
    def run_policy(self, policy, iterations=1):
        pass

    @abc.abstractmethod
    def perform_action(self, state, action):
        pass

    @abc.abstractmethod
    def is_terminal_state(self, state):
        pass

    ##
    #   Add Transition Dynamics
    #
    #   @param values a tuple of the following format ( (state, action), (reward, [(probability, next_state)]) )
    #
    def add_transition_old(self, values):
        if values[0][1] is self.Action.EXIT:
            self._state_actions[(values[0][0], values[0][1])] = values[1]
        else:
            total_probability = 0
            for successor in values[1]:
                total_probability += successor[0]

            if total_probability != 1:
                raise ValueError("Total probabilities should sum to 1")
            else:
                self._state_actions[(values[0][0], values[0][1])] = values[1]

    ##
    #   Add Transition Dynamics
    #
    #   @param values a tuple of the following format ( (state, action), (reward, [(probability, next_state)]) )
    #
    def add_transition(self, state, action, transitions):
        if action is self.Action.EXIT:
            self._state_actions[(state, action)] = transitions
        else:
            if self._is_valid_transitions(transitions):
                self._state_actions[(state, action)] = transitions
            else:
                raise ValueError("Total probabilities should sum to 1")

    ##
    # Returns a list of all available states
    #
    def get_states(self):
        states, actions = zip(*self._state_actions.keys())
        return list(set(states))

    ##
    # Returns a list of all actions for a given state
    # @param state the state
    # @:return actions
    def get_actions(self, state):
        state_actions = self._state_actions.keys()
        return [a for s, a in state_actions if s == state]

    ##
    #
    #
    #
    def get_mdp(self):
        return self._state_actions.copy()

    ##
    #
    #
    def get_transitions(self, state, action):
        return self._state_actions[(state, action)]

    ##
    # Checks if transition probabilities sum to 1
    #
    # @param transitions list of transitions: [(probability, next_state)]
    #
    def _is_valid_transitions(self, transitions):
        total_probability = 0
        for successor in transitions:
            total_probability += successor[0]
        return True if total_probability == 1 else False
