import abc

##
# Abstract Class for all worlds
#


class AbstractWorld(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        self._state_actions = {}

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
        pass;

    ##
    #   Add Transition Dynamics
    #
    #   @param values a tuple of the following format ( (state, action), (reward, [(probability, next_state)]) )
    #
    def add_transition(self, values):
        total_probability = 0
        for successor in values[1][1]:
            total_probability += successor[0]

        if total_probability != 1:
            raise ValueError("Total probabilities should sum to 1")
        else:
            self._state_actions[(values[0][0], values[0][1])] = values[1]


    ##
    # Returns a list of all available states
    #
    def get_states(self):
        pass

    ##
    # Returns a list of all actions for a given state
    # @param state the state
    # @:return actions
    def get_actions(self, state):
        pass

