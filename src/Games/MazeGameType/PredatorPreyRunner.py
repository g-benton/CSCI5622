"""Runs the Predator Prey game."""

import sys
from pathlib import Path
from Prey import Prey
from Predator import Predator
sys.path.append('../../Grid')
from GridConstants import *
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions
from RunConditions import *

def set_up():
    """Set up the world to run.
    Returns: GridWorld object.
    """
    grid_dim = 10
    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, (4, 5))
    wolf = Predator(2, (5, 5), dim = grid_dim)
    # wolf.read_q("Q_matrix.")
    world.add_actor(sheep, (4, 5))
    world.add_actor(wolf, (5, 5))

    # def sheep_producer(actor_id, posn):
    #     return Prey(actor_id, posn)

    # world.add_rule(SpawnNewActorRule(PREY, sheep_producer, time_interval=4))

    return world

def run_sim():
    """Run the simulation."""
    world = set_up()
    condition = NoPreyConditions()
    world.run_simulation(condition, True)

def train_pred(game_count):
    """ Runs game_count number of games to train a single predator """
    grid_dim = 20

    wolf = Predator(2, (0, 0), dim = grid_dim)

    # XXX there is an error in using this, see line 49 in predator.py XXX #
    # wolf.read_q("./wolf_q_mat_50k_training.npy")

    for game in range(game_count):
        # build world
        world = GridWorld((grid_dim, grid_dim))
        sheep = Prey(1, (19, 19))

        # add actors
        wolf.update_posn((0, 0))
        world.add_actor(wolf, (0, 0))
        #for row_ind in range(wolf.q_mat.shape[0]):
            #print(wolf.q_mat[row_ind])
        world.add_actor(sheep, (19, 19))

        condition = NoPreyConditions()
        world.run_simulation(condition, False)


        print("Game", game,  "Done")
        # print(wolf.q_mat)

    wolf.write_q("wolf_q_mat")

    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, (19, 19))

    # add actors
    wolf.update_posn((0, 0))
    world.add_actor(wolf, (0, 0))
    #for row_ind in range(wolf.q_mat.shape[0]):
        #print(wolf.q_mat[row_ind])
    world.add_actor(sheep, (19, 19))

    # condition = TimeLimitConditions(10000)
    condition = NoPreyConditions()
    world.run_simulation(condition, True)



if __name__ == '__main__':
    # run_sim()
    # is this going to work? #

    train_pred(100)
