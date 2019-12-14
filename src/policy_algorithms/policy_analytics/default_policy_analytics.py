from interface import implements
from .policy_analytics import PolicyAnalytics


class DefaultPolicyAnalytics(implements(PolicyAnalytics)):

    def __init__(self):
        self._analytics = {}
        self._analytics["Total States Searched"] = 0
        self._analytics["Total Actions Searched"] = 0
        self._analytics["Convergence Iteration"] = 0
        self.state_complexity = 0
        self.action_complexity = 0
        self.states_searched = 0
        self.actions_searched = 0

    def get_analytics(self):
        return self._analytics.copy()

    def increment_states_searched(self):
        self._analytics["Total States Searched"] += 1

    def increment_action_searched(self):
        self._analytics["Total Actions Searched"] += 1

    def reset(self):
        for key in self._analytics.keys():
            self._analytics[key] = 0

    def set_convergence_iteration(self, iteration_number):
        self._analytics["Convergence Iteration"] = iteration_number

    def add_metric(self, metric, value):
        self._analytics[metric] = value
