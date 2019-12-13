import abc


class PolicyAnalytics:

    def __init__(self):
        self.state_complexity = 0
        self.action_complexity = 0
        self.states_searched = 0
        self.actions_searched = 0
