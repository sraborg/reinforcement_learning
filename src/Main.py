from agent import Agent
from worlds.grid_world import GridWorld
from policy_algorithms.value_iteration import ValueIteration
from policy_algorithms.policy_iteration import PolicyIteration


def main():
    world = GridWorld()
    value_iteration = ValueIteration()
    policy_iteration = PolicyIteration()

    agent1 = Agent(policy_algorithm=value_iteration, world=world)
    agent2 = Agent(policy_algorithm=policy_iteration, world=world)


if __name__ == "__main__":
    main()
