"""Runs the Predator Prey game."""

import sys

from Prey import Prey

sys.path.append('../../Grid')
from GridConstants import *
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions

def set_up():
    """Set up the world to run.
    Returns: GridWorld object.
    """
    world = GridWorld((5, 5), [PREY])
    sheep = Prey(1, (2, 2))
    world.add_actor(sheep, (2, 2))
    return world

def run_sim():
    """Run the simulation."""
    world = set_up()
    condition = TimeLimitConditions(10)
    world.run_simulation(condition)

if __name__ == '__main__':
    run_sim()
