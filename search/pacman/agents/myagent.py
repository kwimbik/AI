from game.controllers import PacManControllerBase
from game.pacman_core import Game, DM

# from game.pac_gui import PacView
import sys
from os.path import dirname

# hack for importing from parent package
sys.path.append(dirname(dirname(dirname(__file__))))
from search_templates import *
from ucs import UCS

# hint: class PacManProblem(Problem)...
#       ... Ucs.search(problem)


class MyAgent(PacManControllerBase):
    def __init__(self, human: bool = False, seed: int = 0) -> None:
        super().__init__(human, seed)

        # You can initialize your own class variables here.

    def tick(self, game: Game) -> None:
        # Your implementation goes here.

        # Dummy implementation: move in a random direction.
        # You won't live long this way
        directions = game.get_possible_pacman_dirs(False)
        self.pacman.set(self.random.choice(directions))
