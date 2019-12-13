from src.user_interfaces.gui_interface import GUIInterface
from tkinter import *


def main():
    # world = GridWorld()
    # value_iteration = ValueIteration()
    # policy_iteration = PolicyIteration()
    # mc = MontyCarlo()
    # #mc.generate_policy(world)
    #
    # #agent1 = Agent(policy_algorithm=value_iteration, world=world)
    # #agent2 = Agent(policy_algorithm=policy_iteration, world=world)
    #
    # print(policy_iteration.generate_policy(world))

    window = Tk()
    window.geometry('500x500')

    app = GUIInterface(window)

    window.mainloop()
    
if __name__ == "__main__":
    main()
