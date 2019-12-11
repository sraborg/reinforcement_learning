from interface import Interface


##
# Policy Algorithm Interface
#

class PolicyAlgorithm(Interface):

    def generate_policy(self, world):
        pass


