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
from matplotlib import pyplot as plt

def set_up():
    """Set up the world to run.
    Returns: GridWorld object.
    """
    grid_dim = 10
    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, (4, 5))
    wolf = Predator(2, (0, 0),
                    [[]], [[]], # predator info
                    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]], [[-135, -90, -45, 0, 45, 90, 135, 180]], # prey info
                    [[]],[[]], # obstacle info
                    [[1, 2, 3, 4, 5, 10, 100],[1,2,3,4,5,10]]) # wall info
    print(wolf.states)
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

    wolf = Predator(2, (0, 0),
                    [[]], [[]], # predator info
                    [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]], [[-135, -90, -45, 0, 45, 90, 135, 180]], # prey info
                    [[]],[[]], # obstacle info
                    [[1, 2, 3, 4, 5, 10, 100],[1,2,3,4,5,10]]) # wall info

    print(wolf.states)


    # XXX there is an error in using this, see line 49 in predator.py XXX #
    # wolf.read_q("./wolf_q_mat_50k_training.npy")

    for game in range(game_count):
        # build world
        world = GridWorld((grid_dim, grid_dim))
        sheep = Prey(1, (19, 19))

        # add actors
        wolf.update_posn((0, 0))
        world.add_actor(wolf, (0, 0))
        world.add_actor(sheep, (19, 19))

        condition = NoPreyConditions()
        world.run_simulation(condition, False)

        print("Game", game + 1,  "Done")

    wolf.write_q("wolf_q_mat")

    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, (19, 19))

    # add actors
    wolf.update_posn((0, 0))
    world.add_actor(wolf, (0, 0))
    world.add_actor(sheep, (19, 19))

    # condition = TimeLimitConditions(10000)
    condition = NoPreyConditions()
    world.run_simulation(condition, True)


def average_moves_over_time(simulations_per_training, max_training):

    """ Stores number of moves over each training iteration for multiple simulations, and averages them """
    simulations = [0 for i in range(max_training)]

    for sim in range(simulations_per_training):

        """ Runs game_count number of games to train a single predator """
        grid_dim = 20

        wolf = Predator(2, (0, 0),
                        [[]], [[]],  # predator info
                        [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]], [[-135, -90, -45, 0, 45, 90, 135, 180]],  # prey info
                        [[]], [[]],  # obstacle info
                        [[1, 2, 3, 4, 5, 10, 100], [1, 2, 3, 4, 5, 10]])  # wall info

        for game in range(max_training):
            # build world
            world = GridWorld((grid_dim, grid_dim))
            sheep = Prey(1, (19, 19))

            # add actors
            wolf.update_posn((0, 0))
            world.add_actor(wolf, (0, 0))
            world.add_actor(sheep, (19, 19))

            condition = NoPreyConditions()
            world.run_simulation(condition, False)

            # store simulated moves
            simulations[game] += world._number_of_moves()

        print("Simulation Number ", sim + 1, "Done")

    # return average moves per training level
    return [float(sim)/simulations_per_training for sim in simulations]

def plot_info(title_, x_axis, y_xis, x_data, y_data, save, display):

    # generate plot
    plt.plot(x_data, y_data)
    plt.ylabel(y_xis)
    plt.xlabel(x_axis)
    plt.title(title_)
    # if you want to save it
    if save:
        plt.savefig(title_)
    if display:
        plt.show()


if __name__ == '__main__':
    # run_sim()
    # is this going to work? #
    train_pred(1000)
    # yes it is
    games_per_sim = 1000
    info = average_moves_over_time(5, games_per_sim)
    plot_info("Average_Moves_Over_time", "Number of Iterations", "Average Number of Moves",
              range(games_per_sim), info, 0, 1)
