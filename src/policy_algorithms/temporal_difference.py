from interface import implements
from .policy_algorithm import PolicyAlgorithm
import random
from operator import itemgetter

class TemporalDifference(implements(PolicyAlgorithm)):
    def __init__(self):
        super().__init__()
        self._world = None
        self._value_table = None
        self._policy_table = None
        self.evaluations = 0
        self.alpha = 0.1    #step size
        self.gamma = 0.1    #learning rate
        self._policy_stable = True
        self.numOfEpisodes = 100

    ##
    # Generates a policy
    #
    # @param world the domain to learn a policy for
    def generate_policy(self, world):
        print("TD")
        self._world = world
        # Initialization
        #take a policy to evaluate
        policy = {None: None}
        #init policy
        for state in world.get_states():
            possible_actions = world.get_actions(state)
            policy[state] = random.choice(possible_actions)

#init all values
        V = {}
        for state in world.get_states():
            if world.is_terminal_state(state):
                V[state] = 0.0
            else:
                V[state] = random.uniform(0,10)

        for loop in range(self.numOfEpisodes):
            #get initial state
            states = world.get_states()
            start_state = random.choice(states)                             # Random Start State
            #create an episode
            episode = world.get_episode(policy, start_state)
            for state,action,reward,next_state in episode:
                #get action A for a state S
                A = policy[state]
                #take A and observe reward R and next state S'
                S_prime, R = world.perform_action(state, A)
                #update value V
                V[state] += self.alpha * (R + (self.gamma * V[S_prime] - V[state]))
                #update state
                if world.is_terminal_state(S_prime):
                    break
        self._extract_policy()
        return self._policy_table.copy()
    pass

    def _extract_policy(self):
        for state in self._world.get_states():
            actions_values = []
            for action in self._world.get_actions(state):
                #self.action_complexity = self.action_complexity + 1
                transitions = self._world.get_transitions(state, action)
                temp_rewards = []

                for probability, next_state in transitions:
                    # Check for Exit Case
                    if next_state is None:
                        temp_rewards.append(self._world.reward(state, action))
                    else:
                        temp_rewards.append(probability * ( self._world.reward(state, action) + self.gamma * self._value_table[next_state]))
                actions_values.append((action, max(temp_rewards)))

            #self.state_complexity = self.state_complexity + 1
            #self.action_complexity = self.action_complexity + 1
            new_action = max(actions_values, key = itemgetter(1))[0]
            self._policy_table[state] = new_action




