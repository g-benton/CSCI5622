"""Runs the Predator Prey game."""

import sys
from pathlib import Path
from Prey import Prey
from Baseline_Predator import Predator
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
    wolf = Predator(1, (grid_dim, grid_dim), dim=grid_dim, )
    sheep = Prey(2, (0, 0),
                    [[1, 2, 3, 4, 5, 7, 9, 100]], [[-135, -90, -45, 0, 45, 90, 135, 180]],
                    [[1, 2, 3, 4, 5, 10, 100],[1,2,3,4,5,10]])
    # wolf.read_q("Q_matrix.")
    world.add_actor(sheep, (0, 0))
    world.add_actor(wolf, (grid_dim, grid_dim))

    # def sheep_producer(actor_id, posn):
    #     return Prey(actor_id, posn)

    # world.add_rule(SpawnNewActorRule(PREY, sheep_producer, time_interval=4))

    return world

def run_sim():
    """Run the simulation."""
    world = set_up()
    condition = NoPreyConditions()
    world.run_simulation(condition, True)

def average_move_tester(game_count=1000, average_count=10):
    """ Runs game_count number of games to train a single predator """

    grid_dim = 10

    move_counts = [[None]*average_count]*game_count

    # XXX there is an error in using this, see line 49 in predator.py XXX #
    # wolf.read_q("./wolf_q_mat_50k_training.npy")
    for test in range(average_count):
        sheep = Prey(2, (19, 19),
        [[1, 2, 3, 4, 5, 7, 9, 100]], [[-135, -90, -45, 0, 45, 90, 135, 180]],
        [[1, 2, 3, 4, 5, 10, 100],[1,2,3,4,5,10]])
        wolf = Predator(1, (0, 0), dim = grid_dim)
        for game in range(game_count):
            # build world
            world = GridWorld((grid_dim, grid_dim))

            # add actors
            wolf.update_posn((0, 0))
            world.add_actor(wolf, (0, 0))
            #for row_ind in range(wolf.q_mat.shape[0]):
                #print(wolf.q_mat[row_ind])
            sheep.update_posn((19, 19))
            world.add_actor(sheep, (19, 19))

            # condition = TimeLimitConditions(1000)
            # condition = NoPreyConditions()
            condition = CombinedConditions(1000)
            world.run_simulation(condition, False)

            move_counts[test][game] = world._number_of_moves()

    return move_counts

if __name__ == '__main__':
    # run_sim()
    # is this going to work? #

    move_counts = average_move_tester(10, 1)

    average_moves = [sum(iter)/len(iter) for iter in move_counts]

    plt.plot(average_moves)
    plt.ylabel("Average Moves per Game (1000 max.)")
    plt.xlabel("Number of Games Trained")
    plt.title("Prey Q-Learning Model")
    plt.show()
