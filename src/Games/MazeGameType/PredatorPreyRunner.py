"""Runs the Predator Prey game."""

import sys
from pathlib import Path
from Prey import Prey
from Predator import Predator
from Obstacle import Obstacle
sys.path.append('../../Grid')
from GridConstants import *
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions
from RunConditions import *
from matplotlib import pyplot as plt
from copy import deepcopy

def set_up():
    """Set up the world to run.
    Returns: GridWorld object.
    """
    grid_dim = 10
    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, (4, 5))
    wolf = Predator(2, (5, 5), dim = grid_dim)
    rock = Obstacle(3, (3, 3), dim = grid_dim)

    # wolf.read_q("Q_matrix.")
    world.add_actor(sheep, (4, 5))
    world.add_actor(wolf, (5, 5))
    world.add_actor(rock, (3, 3))


    # def sheep_producer(actor_id, posn):
    #     return Prey(actor_id, posn)

    # world.add_rule(SpawnNewActorRule(PREY, sheep_producer, time_interval=4))

    return world

def run_sim():
    """Run the simulation."""
    world = set_up()
    condition = NoPreyConditions()
    world.run_simulation(condition, True)

def create_checker_maze(size, predator_start, prey_start):
    obstacles = {}
    counter = 0
    for i in range(size):
        for j in range(size):
            if j % 2 != 0:
                if i % 2 == 0:
                    if str((i,j)) not in predator_start and str((i,j)) not in prey_start:
                        obstacles[counter] = (i,j)
                        counter += 1
    return obstacles

def train_pred_in_maze(game_count, maze, grid_dim, pred_position, prey_position, disp):

    """ Runs game_count number of games to train a single predator """
    wolf = Predator(-1, pred_position, dim=grid_dim)

    # create list of obstacles and there position from maze
    obstacles = []
    for rock in maze.keys():
        new = Obstacle(rock, maze[rock], dim=grid_dim)
        obstacles.append(deepcopy(new))

    for game in range(game_count):
        # build world
        world = GridWorld((grid_dim, grid_dim))
        sheep = Prey(-2, prey_position)

        # add actors
        wolf.update_posn(pred_position)
        world.add_actor(wolf, pred_position)
        world.add_actor(sheep, prey_position)

        # overlay maze
        counter = 0
        for obstacle in obstacles:
            world.add_actor(obstacle, maze[counter])
            counter += 1

        condition = NoPreyConditions()
        world.run_simulation(condition, False)

        #print("Game", game, "Done")

    wolf.write_q("wolf_q_mat")
    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(-2, prey_position)

    # add actors
    wolf.update_posn(pred_position)
    world.add_actor(wolf, pred_position)
    world.add_actor(sheep, prey_position)

    # overlay maze
    counter = 0
    for obstacle in obstacles:
        world.add_actor(obstacle, maze[counter])
        counter += 1

    # condition = TimeLimitConditions(10000)
    condition = NoPreyConditions()
    world.run_simulation(condition, disp)
    return world, world._number_of_moves()

def average_moves_over_time(simulations_per_training, max_training,
                            grid_dim, pred_position, prey_position, maze):

    """ Stores number of moves over each training iteration for multiple simulations, and averages them """
    simulations = [0 for i in range(max_training)]

    for training in range(max_training):
        for sim in range(simulations_per_training):
            world, number_of_moves = train_pred_in_maze(max_training, maze, grid_dim, pred_position, prey_position, 0)
            simulations[training] += number_of_moves
        simulations[training] = simulations[training]/simulations_per_training

        print("Number of training iterations: ", training)
        print("Average number of moves: ", simulations[training])

    # return average moves per training level
    return simulations

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

    ### constants
    game_count = 1000
    simulations = 10
    grid_dim = 11
    prey_position = (9,9)
    pred_position = (0,0)

    # vanilla run
    # run_sim()

    # checker maze run
    predator_start = [str(pred_position)]
    prey_start = [str(prey_position)]
    maze = create_checker_maze(grid_dim, predator_start, prey_start)
    train_pred_in_maze(game_count, maze, grid_dim, pred_position, prey_position, 1)
    #info = average_moves_over_time(simulations, game_count,grid_dim, pred_position, prey_position, maze)
    #plot_info("Average_Moves_Over_time", "Number of Iterations", "Average Number of Moves", range(10), info, 0, 1)


