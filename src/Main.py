from agent import Agent
from worlds.grid_world import GridWorld
from policy_algorithms.value_iteration import ValueIteration
from policy_algorithms.policy_iteration import PolicyIteration
from policy_algorithms.monty_carlo import MontyCarlo


def main():
    world = GridWorld()
    #value_iteration = ValueIteration()
    policy_iteration = PolicyIteration()
    mc = MontyCarlo()
    #mc.generate_policy(world)

    #agent1 = Agent(policy_algorithm=value_iteration, world=world)
    #agent2 = Agent(policy_algorithm=policy_iteration, world=world)

    print(mc.generate_policy(world))

    
if __name__ == "__main__":
    main()
