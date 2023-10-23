#!/usr/bin/env python3
from game.controllers import PacManControllerBase
from game.pacman import Game, DM, Direction
from typing import List
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from search_templates import *
from ucs import ucs


class PacProblem(Problem):
    def __init__(self, game: Game) -> None:
        self.game: Game = game

    def initial_state(self) -> int:
        return self.game.pac_loc

    def actions(self, state: int) -> List[int]:
        return [0,1,2,3]

    def result(self, state: int, action: int) -> int:
        return self.game.get_neighbor(state, action)

    def is_goal(self, state: int) -> bool:
        active_pills = self.game.get_active_pills_nodes()
        active_power_pills = self.game.get_active_power_pills_nodes()
        ghost_locs = self.game.ghost_locs
        fruit = self.game.fruit_loc
        targets = active_pills + active_power_pills
        if (fruit != -1): targets += [fruit]
        if self.game.eating_time > 2:
            for g in range(self.game.NUM_GHOSTS):
                if (self.game.is_edible(g)): targets += [ghost_locs[g]]
        nearest = self.game.get_target(self.game.pac_loc, targets, True, DM.PATH)
        if state == nearest: return True
        return False

    def cost(self, state: int, action: int) -> float:
        loc =  self.game.get_neighbor(state, action)
        ghost_locations = self.game.ghost_locs
        distances = [self.game.get_path_distance(X, loc) for X in ghost_locations]
        for d in distances:
            if d < 3 and self.game.eating_time < 2: 
                return 100
        return 1


class Agent_Using_UCS(PacManControllerBase):
    def tick(self, game: Game) -> None:
        prob = PacProblem(game)
        sol = ucs(prob)
        if sol is None or not sol.actions:
            pass
            # if self.verbose:
            #     print("No path found.", file=sys.stderr)
        else:
            self.pacman.set(sol.actions[0])
