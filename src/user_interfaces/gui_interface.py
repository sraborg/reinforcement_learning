from interface import implements
from src.user_interfaces.user_interface import UserInterface
from tkinter import *

##
# GUI User Interface
#
from src.policy_algorithms.policy_iteration import PolicyIteration
from src.worlds.grid_world import GridWorld


class GUIInterface(implements(UserInterface)):

    def __init__(self, window=None):
        self._window = window
        self._world = GridWorld()
        self._currentPolicyAlgorithm = None
        self._policyAlgorithm = {}
        self.init_window()

    def generatePolicy(self):
        policy = self._currentPolicyAlgorithm.generate_policy(self._world)
        print(policy)

    def onSelectPolicyIteration(self):
        if "policyIteration" not in self._policyAlgorithm.keys():
            self._policyAlgorithm["PolicyIteration"] = PolicyIteration()
        self._currentPolicyAlgorithm = self._policyAlgorithm["PolicyIteration"]

        print("PI Selected")

    def onSelectValueIteration(self):
        if "policyIteration" not in self._policyAlgorithm.keys():
            self._policyAlgorithm["ValueIteration"] = PolicyIteration()
        self._currentPolicyAlgorithm = self._policyAlgorithm["ValueIteration"]

        print("VI Selected")

    def onSelectMonteCarlo(self):
        if "policyIteration" not in self._policyAlgorithm.keys():
            self._policyAlgorithm["MonteCarlo"] = PolicyIteration()
        self._currentPolicyAlgorithm = self._policyAlgorithm["MonteCarlo"]

        print("Monte Carlo Selected")


    def init_window(self):
        self._window.title("GRID WORLD")

        #creating menubutton
        Menubar = Menu(self._window)
        policy_menu = Menu(Menubar, tearoff=0)
        policy_menu.add_command(label = "Policy Iteration", command = self.onSelectPolicyIteration)
        policy_menu.add_command(label = "Value Iteration", command = self.onSelectValueIteration)
        policy_menu.add_command(label = "Monte Carlo", command = self.onSelectMonteCarlo)

        #adding a parent element to the menu
        Menubar.add_cascade(label="Choose a Policy", menu = policy_menu)

        self._window.config(menu = Menubar)

        #creating button
        genPolicyButton = Button(self._window, text = "Generate Policy", command = self.generatePolicy)

        genPolicyButton.pack()





