import abc

##
# Abstract Class for all worlds
#


class AbstractWorld(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __init__(self):
        pass

    @property
    def states(self):
        raise NotImplementedError

    @property
    def state_actions(self, state):
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

