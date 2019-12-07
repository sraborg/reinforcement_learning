##
# Our agent class
#
#


class Agent:

    ##
    # Constructor
    # @param a keyword dictionary with optional
    #
    def __init__(self, **keyword_parameters):

        self.policy_algorithm = None
        self.world = None
        self.policy = None

        if "policy_algorithm" in keyword_parameters:
            self.policy_algorithm = keyword_parameters["policy_algorithm"]
            print("Policy Set")

        if "world" in keyword_parameters:
            self.world = keyword_parameters["world"]
            print("World Set")

    ##
    # Mutator: Sets policy attribute
    #
    def set_policy(self, policy_):
        self.policy = policy_

    ##
    # Mutator: Set world attribute
    #
    #
    def set_world(self, world_):
        self.world = world_

    ##
    # Generates a new policy for the set world using the set policyAlgorithm
    #
    def generate_policy(self):
        self.policy = self.policy_algorithm.generate_policy()
