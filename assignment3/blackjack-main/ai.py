import copy
import random
import math
import matplotlib.pyplot as plt

from game import Game, states

HIT = 0
STAND = 1
DISCOUNT = 0.95 #This is the gamma value for all value calculations

class Agent:
    def __init__(self):

        # For MC values
        self.MC_values = {} # Dictionary: Store the MC value of each state
        self.S_MC = {}      # Dictionary: Store the sum of returns in each state
        self.N_MC = {}      # Dictionary: Store the number of samples of each state
        # MC_values should be equal to S_MC divided by N_MC on each state (important for passing tests)

        # For TD values
        self.TD_values = {}  # Dictionary storing the TD value of each state
        self.N_TD = {}       # Dictionary: Store the number of samples of each state

        # For Q-learning values
        self.Q_values = {}   # Dictionary storing the Q-Learning value of each state and action
        self.N_Q = {}        # Dictionary: Store the number of samples of each state

        # Initialization of the values
        for s in states:
            self.MC_values[s] = 0
            self.S_MC[s] = 0
            self.N_MC[s] = 0
            self.TD_values[s] = 0
            self.N_TD[s] = 0
            self.Q_values[s] = [0,0] # First element is the Q value of "Hit", second element is the Q value of "Stand"
            self.N_Q[s] = 0
        # NOTE: see the comment of `init_cards()` method in `game.py` for description of game state       
        self.simulator = Game()

    # NOTE: do not modify
    # This is the policy for MC and TD learning. 
    @staticmethod
    def default_policy(state):
        user_sum = state[0]
        user_A_active = state[1]
        actual_user_sum = user_sum + user_A_active * 10
        if actual_user_sum < 14:
            return 0
        else:
            return 1

    # NOTE: do not modify
    # This is the fixed learning rate for TD and Q learning. 
    @staticmethod
    def alpha(n):
        return 10.0/(9 + n)
    
    def MC_run(self, num_simulation, tester=False):
        state_A = (10,0,1)
        state_B = (20,0,1)
        MC_vec_A = []
        MC_vec_B = []
        N_vec_A = []
        N_vec_B = []

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "MC")
            self.simulator.reset()  # Restart the simulator

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: Go through game.py file and figure out which functions will be useful
            # Useful variables:
            #     - DISCOUNT
            #     - self.MC_values     (read comments in self.__init__)
            # remember to update self.MC_values, self.S_MC, self.N_MC for the autograder!

            episode = self.simulator.simulate_sequence(self.default_policy)
            # print(episode)
            len_episode = len(episode)

            for i in range(len_episode):
                s, r = episode[i]
                self.N_MC[s] += 1
                for j in range(i, len_episode):
                    self.S_MC[s] = self.S_MC[s] + pow(DISCOUNT, j-i) * episode[j][1]

                if (s == state_A):
                    MC_vec_A.append(self.S_MC[s] / self.N_MC[s])
                    N_vec_A.append(self.N_MC[s])
                elif (s == state_B):
                    MC_vec_B.append(self.S_MC[s] / self.N_MC[s])
                    N_vec_B.append(self.N_MC[s])

        # after all the simulations, take the average
        for s in states:
            if self.N_MC[s] > 0:
                self.MC_values[s] = self.S_MC[s] / self.N_MC[s]

        # PLOTTING CODE
        fig = plt.figure()
        plt.plot(N_vec_A, MC_vec_A)
        plt.title('MC: Value Estimate VS Number of Visits (s = A (10,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.show()
        # fig.savefig("plots/MC_value_vs_visit_state_A.png")

        fig = plt.figure()
        plt.plot(N_vec_B, MC_vec_B)
        plt.title('MC: Value Estimate VS Number of Visits (s = B (20,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.show()
        # fig.savefig("plots/MC_value_vs_visit_state_B.png")

    
    def TD_run(self, num_simulation, tester=False):
        state_A = (10,0,1)
        state_B = (20,0,1)
        TD_vec_A = []
        N_vec_A = []
        TD_vec_B = []
        N_vec_B = []

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "TD")
            self.simulator.reset()

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: Go through game.py file and figure out which functions will be useful
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Useful variables/funcs:
            #     - DISCOUNT
            #     - self.TD_values  (read comments in self.__init__)
            # remember to update self.TD_values and self.N_TD for the autograder!
            s = self.simulator.state

            while s is not None:
                action = self.default_policy(s)
                
                R = self.simulator.check_reward()
                next_s, _ = self.simulator.simulate_one_step(action)

                if next_s is None:
                    self.TD_values[next_s] = 0

                self.N_TD[s] += 1
                self.TD_values[s] = self.TD_values[s] + self.alpha(self.N_TD[s]) * (R + DISCOUNT * self.TD_values[next_s] - self.TD_values[s])

                if (s == state_A):
                    TD_vec_A.append(self.TD_values[s])
                    N_vec_A.append(self.N_TD[s])
                elif (s == state_B):
                    TD_vec_B.append(self.TD_values[s])
                    N_vec_B.append(self.N_TD[s])

                s = next_s

        # PLOTTING CODE
        fig = plt.figure()
        plt.plot(N_vec_A, TD_vec_A)
        plt.title('TD: Value Estimate VS Number of Visits (s = A (10,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.show()
        # fig.savefig("plots/TD_value_vs_visit_state_A.png")

        fig = plt.figure()
        plt.plot(N_vec_B, TD_vec_B)
        plt.title('TD: Value Estimate VS Number of Visits (s = B (20,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.show()
        # fig.savefig("plots/TD_value_vs_visit_state_B.png")

                
    def Q_run(self, num_simulation, tester=False):
        state_A = (10,0,1)
        state_B = (20,0,1)
        
        Q_vec_A_0 = []
        Q_vec_A_1 = []
        N_vec_A = []
        Q_vec_B_0 = []
        Q_vec_B_1 = []
        N_vec_B = []

        # Perform num_simulation rounds of simulations in each cycle of the overall game loop
        for simulation in range(num_simulation):
            # Do not modify the following three lines
            if tester:
                self.tester_print(simulation, num_simulation, "Q")
            self.simulator.reset()

            # TODO
            # Note: Do not reset the simulator again in the rest of this simulation
            # Hint: Go through game.py file and figure out which functions will be useful
            # Hint: The learning rate alpha is given by "self.alpha(...)"
            # Hint: Implement epsilon-greedy method in "self.pick_action(...)"
            # Useful variables:
            #     - DISCOUNT
            #     - self.Q_values  (read comments in self.__init__)
            # remember to update self.Q_values, self.N_Q for the autograder!

            epsilon = 0.4
            s = self.simulator.state
            
            while s is not None:
                action = self.pick_action(s, epsilon)
                R = self.simulator.check_reward()

                next_s, _ = self.simulator.simulate_one_step(action)

                if next_s is None:
                    self.Q_values[next_s] = [0,0]

                self.N_Q[s] += 1
                self.Q_values[s][action] = self.Q_values[s][action] + self.alpha(self.N_Q[s]) * (R + DISCOUNT * max(self.Q_values[next_s][0], self.Q_values[next_s][1]) - self.Q_values[s][action])

                if (s == state_A):
                    Q_vec_A_0.append(self.Q_values[s][0])
                    Q_vec_A_1.append(self.Q_values[s][1])
                    N_vec_A.append(self.N_Q[s])
                elif (s == state_B):
                    Q_vec_B_0.append(self.Q_values[s][0])
                    Q_vec_B_1.append(self.Q_values[s][1])
                    N_vec_B.append(self.N_Q[s])

                s = next_s

        # PLOTTING CODE
        plt.gca().set_color_cycle(['red', 'blue'])
        fig = plt.figure()
        plt.plot(N_vec_A, Q_vec_A_0, "r")
        plt.plot(N_vec_A, Q_vec_A_1, "b")
        plt.title('Q-Learning: Value Estimate VS Number of Visits (s = A (10,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.legend(["Action - HIT", "Action - STAND"])
        plt.show()
        # fig.savefig("plots/Q_value_vs_visit_state_A.png")

        fig = plt.figure()
        plt.plot(N_vec_B, Q_vec_B_0, "r")
        plt.plot(N_vec_B, Q_vec_B_1, "b")
        plt.title('Q-Learning: Value Estimate VS Number of Visits (s = B (20,0,1))')
        plt.xlabel('Number of Visits to State')
        plt.ylabel('V(s)')
        plt.grid(linestyle = '--')
        plt.legend(["Action - HIT", "Action - STAND"])
        plt.show()
        # fig.savefig("plots/Q_value_vs_visit_state_B.png")


    def pick_action(self, s, epsilon):
        # TODO: Replace the following random return value with the epsilon-greedy strategy
        if (random.random() < epsilon):
            return random.randint(0, 1)
        else:
            if self.Q_values[s][0] > self.Q_values[s][1]:
                return 0
            else:
                return 1


    #Note: do not modify
    def autoplay_decision(self, state):
        hitQ, standQ = self.Q_values[state][HIT], self.Q_values[state][STAND]
        if hitQ > standQ:
            return HIT
        if standQ > hitQ:
            return STAND
        return HIT #Before Q-learning takes effect, just always HIT

    # NOTE: do not modify
    def save(self, filename):
        with open(filename, "w") as file:
            for table in [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q]:
                for key in table:
                    key_str = str(key).replace(" ", "")
                    entry_str = str(table[key]).replace(" ", "")
                    file.write(f"{key_str} {entry_str}\n")
                file.write("\n")

    # NOTE: do not modify
    def load(self, filename):
        with open(filename) as file:
            text = file.read()
            MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text, _  = text.split("\n\n")
            
            def extract_key(key_str):
                return tuple([int(x) for x in key_str[1:-1].split(",")])
            
            for table, text in zip(
                [self.MC_values, self.TD_values, self.Q_values, self.S_MC, self.N_MC, self.N_TD, self.N_Q], 
                [MC_values_text, TD_values_text, Q_values_text, S_MC_text, N_MC_text, NTD_text, NQ_text]
            ):
                for line in text.split("\n"):
                    key_str, entry_str = line.split(" ")
                    key = extract_key(key_str)
                    table[key] = eval(entry_str)

    # NOTE: do not modify
    @staticmethod
    def tester_print(i, n, name):
        print(f"\r  {name} {i + 1}/{n}", end="")
        if i == n - 1:
            print()
