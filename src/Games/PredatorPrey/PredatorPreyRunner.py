"""Runs the Predator Prey game."""

import sys

from Prey import Prey
from Predator import Predator
sys.path.append('../../Grid')
from GridConstants import *
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions

def set_up():
    """Set up the world to run.
    Returns: GridWorld object.
    """
    grid_dim = 10
    world = GridWorld((grid_dim, grid_dim), [PREY, PREDATOR])
    sheep = Prey(1, (4, 5))
    wolf = Predator(2, (5, 5), dim = grid_dim)
    world.add_actor(sheep, (4, 5))
    world.add_actor(wolf, (5, 5))
    return world

def run_sim():
    """Run the simulation."""
    world = set_up()
    condition = TimeLimitConditions(10000)
    world.run_simulation(condition, True)

if __name__ == '__main__':
    run_sim()
    # is this going to work? #
