#!/usr/bin/env python

"""code template"""

import random
import numpy as np

from graphics import *
from gridutil import *

import agents


class LocWorldEnv:
    actions = "turnleft turnright forward".split()

    def __init__(self, size, walls, gold, pits, eps_perc, eps_move, start_loc):
        self.size = size
        self.walls = walls
        self.gold = gold
        self.pits = pits
        self.action_sensors = []
        self.locations = {*locations(self.size)}.difference(self.walls)
        self.eps_perc = eps_perc
        self.eps_move = eps_move
        self.start_loc = start_loc
        self.lifes = 3
        self.reset()
        self.finished = False

    def reset(self):
        self.agentLoc = self.start_loc
        self.agentDir = 'N'

    def getPercept(self):
        p = self.action_sensors
        self.action_sensors = []
        for dir in ORIENTATIONS:
            nh = nextLoc(self.agentLoc, dir)
            prob = 0.0 + self.eps_perc
            if (not legalLoc(nh, self.size)) or nh in self.walls:
                prob = 1.0 - self.eps_perc
            if random.random() < prob:
                p.append(dir)

        for dir in ORIENTATIONS:
            nh = nextLoc(self.agentLoc, dir)
            if nh in self.pits and 'breeze' not in p:
                p.append('breeze')

        if self.agentLoc in self.pits:
            p.append('pit')

        return p

    def doAction(self, action):
        points = -1

        rand_val = random.random()
        if rand_val < self.eps_move:
            action = nextDirection(action, -1)
        elif rand_val < 2 * self.eps_move:
            action = nextDirection(action, 1)

        loc = nextLoc(self.agentLoc, action)
        if legalLoc(loc, self.size) and (loc not in self.walls):
            self.agentLoc = loc
        else:
            self.action_sensors.append("bump")

        if self.agentLoc in self.pits:
            self.lifes -= 1
            self.reset()
            points -= 10
            if self.lifes == 0:
                self.finished = True
            print('You stepped into a pit')

        if self.agentLoc == self.gold:
            points += 20
            self.finished = True
            print('You found gold!')

        return points  # cost/benefit of action

    # def finished(self):
    #     return False


class LocView:
    # LocView shows a view of a LocWorldEnv. Just hand it an env, and
    #   a window will pop up.

    Size = .2
    Points = {'N': (0, -Size, 0, Size), 'E': (-Size, 0, Size, 0),
              'S': (0, Size, 0, -Size), 'W': (Size, 0, -Size, 0)}

    color = "black"

    def __init__(self, state, height=800, title="Loc World"):
        xySize = state.size
        win = self.win = GraphWin(title, 1.33 * height, height, autoflush=False)
        win.setBackground("gray99")
        win.setCoords(-.5, -.5, 1.33 * xySize - .5, xySize - .5)
        cells = self.cells = {}
        for x in range(xySize):
            for y in range(xySize):
                cells[(x, y)] = Rectangle(Point(x - .5, y - .5), Point(x + .5, y + .5))
                cells[(x, y)].setWidth(2)
                cells[(x, y)].draw(win)
        self.agt = None
        self.arrow = None
        ccenter = 1.167 * (xySize - .5)
        # self.time = Text(Point(ccenter, (xySize - 1) * .75), "Time").draw(win)
        # self.time.setSize(36)
        # self.setTimeColor("black")

        self.agentName = Text(Point(ccenter, (xySize - 1) * .5), "").draw(win)
        self.agentName.setSize(20)
        self.agentName.setFill("Orange")

        self.info = Text(Point(ccenter, (xySize - 1) * .25), "").draw(win)
        self.info.setSize(20)
        self.info.setFace("courier")

        self.update(state)

    def setAgent(self, name):
        self.agentName.setText(name)

    # def setTime(self, seconds):
    #     self.time.setText(str(seconds))

    def setInfo(self, info):
        self.info.setText(info)

    def update(self, state, P=None, pi=None):
        # View state in exiting window
        for loc, cell in self.cells.items():
            if loc in state.walls:
                cell.setFill("black")
            elif loc == state.gold:
                cell.setFill("yellow")
            elif loc in state.pits:
                cell.setFill("gray")
            else:
                if P is None:
                    cell.setFill("white")
                else:
                    c = int(round(P[loc[0], loc[1]] * 255))
                    cell.setFill('#ff%02x%02x' % (255 - c, 255 - c))

        if self.agt:
            self.agt.undraw()
        if state.agentLoc:
            self.agt = self.drawArrow(state.agentLoc, state.agentDir, 10, self.color)

        if pi:
            for loc, cell in self.cells.items():
                if loc in pi:
                    self.drawArrow(loc, pi[loc], 3, 'green')

    def drawArrow(self, loc, heading, width, color):
        x, y = loc
        dx0, dy0, dx1, dy1 = self.Points[heading]
        p1 = Point(x + dx0, y + dy0)
        p2 = Point(x + dx1, y + dy1)
        a = Line(p1, p2)
        a.setWidth(width)
        a.setArrow('last')
        a.setFill(color)
        a.draw(self.win)
        return a

    def pause(self):
        self.win.getMouse()

    # def setTimeColor(self, c):
    #     self.time.setTextColor(c)

    def close(self):
        self.win.close()


def main():
    random.seed(13)
    # rate of executing actions
    rate = 1
    # chance that perception will be wrong
    eps_perc = 0.1
    # chance that the agent will not move forward despite the command
    eps_move = 0.05
    # number of actions to execute
    n_steps = 40
    # size of the environment
    env_size = 16
    # map of the environment: 1 - wall, 0 - free
    map = np.array([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
    # build the list of walls locations
    walls = []
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i, j] == 1:
                walls.append((j, env_size - i - 1))

    ngames = 10
    step_lim = 50
    npits = 3
    start_loc = (0, 6)
    all_points = 0
    for g in range(ngames):
        game_points = 0

        locs = list({*locations(env_size)}.difference(walls).difference([start_loc]))

        # first drawn location is gold location
        locs_ch = random.sample(locs, k=1 + npits)
        # location of gold
        gold = locs_ch[0]
        # locations of pits
        pits = locs_ch[1:]

        # create the environment and viewer
        env = LocWorldEnv(env_size, walls, gold, pits, eps_perc, eps_move, start_loc)
        view = LocView(env)

        # create the agent
        agent = agents.prob.LocAgent(env.size, env.walls, eps_move, start_loc)
        t = 0
        while not env.finished and t < step_lim:
            print('step %d' % t)

            percept = env.getPercept()
            # agent has to know its location, so pass it as argument
            action = agent(percept, env.agentLoc)

            print('\nPercept: ', percept)
            print('Action ', action)
            print('Location ', env.agentLoc)
            print('current game points = ', game_points)

            pi = agent.get_policy()
            view.update(env, pi=pi)
            update(rate)
            # uncomment to pause before action
            # view.pause()

            game_points += env.doAction(action)

            t += 1

        # after the last action - possibility to update pits location
        percept = env.getPercept()
        agent(percept, env.agentLoc)
        pi = agent.get_policy()
        view.update(env, pi=pi)

        print('\n\nfinal game points = ', game_points)
        all_points += game_points
        # pause until mouse clicked
        view.pause()
        view.win.close()

    print('\n\n\naverage game points = ', all_points / ngames)


if __name__ == '__main__':
    main()
