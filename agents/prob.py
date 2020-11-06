# prob.py
# This is

import random
import numpy as np

from gridutil import *


class LocAgent:

    def __init__(self, size, walls, eps_move, npits, loc):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {iloc: idx for idx, iloc in enumerate(self.locations)}
        self.eps_move = eps_move
        self.npits = npits
        self.loc = loc

        # previous action
        self.prev_action = None

        self.t = 0

        self.V = np.zeros([len(self.locations)], dtype=np.float)
        self.pi = ['E' for _ in self.locations]

        # TODO PUT YOUR ADDITIONAL VARIABLES HERE


        # ---------------------------------------

        self.comp_value_and_policy()

    def comp_value_and_policy(self):
        reward_gold = 10
        reward_pits = -100
        gamma = 0.9
        eps_V = 1e-6

        iter = 0
        
        # compute self.V and self.pi
        # TODO PUT YOUR CODE HERE


        # -----------------------

        print('Policy found after ', iter, ' iterations')

    def get_policy(self):
        pi_dict = {loc: self.pi[i] for i, loc in enumerate(self.locations)}
        return pi_dict

    def __call__(self, percept, loc):
        self.loc = loc

        # update the policy
        # TODO PUT YOUR CODE HERE


        # -----------------------

        # choose action according to policy
        action = self.pi[self.loc_to_idx[self.loc]]

        return action

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
