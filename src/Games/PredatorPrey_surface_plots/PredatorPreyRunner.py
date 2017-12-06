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
from numpy import linspace
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def set_up(epsilon = None, gamma = None, alpha = None, wolf_start = (0,0), grid_dim = 20, sheep_start = (19,19)):
    """Set up the world to run.
    Returns: GridWorld object.
    """
    grid_dim = grid_dim
    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, sheep_start)
    wolf = Predator(2, wolf_start, grid_dim, epsilon, gamma, alpha)
    # wolf.read_q("Q_matrix.")
    world.add_actor(sheep, sheep_start)
    world.add_actor(wolf, wolf_start)

    # def sheep_producer(actor_id, posn):
    #     return Prey(actor_id, posn)

    # world.add_rule(SpawnNewActorRule(PREY, sheep_producer, time_interval=4))

    return world

def run_sim(epsilon = None, gamma = None, alpha = None, wolf_start = (0,0), grid_dim = 20, sheep_start = (19,19)):
    """Run the simulation."""
    world = set_up(epsilon, gamma, alpha, wolf_start, grid_dim, sheep_start)
    condition = NoPreyConditions()
    world.run_simulation(condition, True)

def train_pred(game_count, epsilon = None, gamma = None, alpha = None, wolf_start = (0,0), grid_dim = 20, sheep_start = (19,19)):
    """ Runs game_count number of games to train a single predator """

    wolf = Predator(2, wolf_start, grid_dim, epsilon, gamma, alpha)

    # XXX there is an error in using this, see line 49 in predator.py XXX #
    # wolf.read_q("./wolf_q_mat_50k_training.npy")

    for game in range(game_count):
        # build world
        world = GridWorld((grid_dim, grid_dim))
        sheep = Prey(1, sheep_start)

        # add actors
        wolf.update_posn(wolf_start)
        world.add_actor(wolf, wolf_start)
        world.add_actor(sheep, sheep_start)

        condition = NoPreyConditions()
        world.run_simulation(condition, False)

        print("Game", game,  "Done")
        # print(wolf.q_mat)

    wolf.write_q("wolf_q_mat")

    world = GridWorld((grid_dim, grid_dim))
    sheep = Prey(1, sheep_start)

    # add actors
    wolf.update_posn(wolf_start)
    world.add_actor(wolf, wolf_start)
    #for row_ind in range(wolf.q_mat.shape[0]):
        #print(wolf.q_mat[row_ind])
    world.add_actor(sheep, sheep_start)

    # condition = TimeLimitConditions(10000)
    condition = NoPreyConditions()
    world.run_simulation(condition, True)

def average_moves_over_time(simulations_per_training, max_training,
                            epsilon = None, gamma = None, alpha = None, wolf_start = (0,0), grid_dim = 20, sheep_start = (19,19)):

    """ Stores number of moves over each training iteration for multiple simulations, and averages them """
    simulations = [0 for i in range(max_training)]

    for sim in range(simulations_per_training):

        """ Runs game_count number of games to train a single predator """

        wolf = Predator(2, wolf_start, grid_dim, epsilon, gamma, alpha)

        for game in range(max_training):
            # build world
            world = GridWorld((grid_dim, grid_dim))
            sheep = Prey(1, sheep_start)

            # add actors
            wolf.update_posn(wolf_start)
            world.add_actor(wolf, wolf_start)
            world.add_actor(sheep, sheep_start)

            condition = NoPreyConditions()
            world.run_simulation(condition, False)

            # store simulated moves
            simulations[game] += world._number_of_moves()

        print("Simulation Number ", sim, "Done")

    # return average moves per training level
    return [float(sim)/simulations_per_training for sim in simulations]

def generate_surface_plots(steady_state, smoothness, grid_spacing, gamma_range = [0,1], epsilon_range = [0,1], alpha_range = [0,1]):


    if (gamma_range is not None) and (alpha_range is not None):
        grid_gamma = linspace(gamma_range[0], gamma_range[1], grid_spacing)
        grid_epsilon = linspace(alpha_range[0], alpha_range[1], grid_spacing)
    elif (gamma_range is not None) and (epsilon_range is not None):
        grid_gamma = linspace(gamma_range[0], gamma_range[1], grid_spacing)
        grid_epsilon = linspace(epsilon_range[0], epsilon_range[1], grid_spacing)
    elif (alpha_range is not None) and (epsilon_range is not None):
        grid_gamma = linspace(alpha_range[0], alpha_range[1], grid_spacing)
        grid_epsilon = linspace(epsilon_range[0], epsilon_range[1], grid_spacing)
    else:
        print('to much info, check yourself before you reck your self')
        return None

    grid_info = []
    for epsilon in grid_epsilon:
        info = []
        for gamma in grid_gamma:
            info.append(average_moves_over_time(smoothness, steady_state, epsilon, gamma)[-1])
            print('currently on: epsilon = '+ str(epsilon) + ' and gamma = ' + str(gamma))
        grid_info.append(info)

    data = np.array([[stat for stat in higher_stats] for higher_stats in grid_info])
    length = data.shape[0]
    width = data.shape[1]
    x, y = np.meshgrid(np.array(grid_gamma), np.array(grid_epsilon))
    fig1 = plt.figure()
    ax = fig1.add_subplot(1,1,1, projection='3d')
    ax.plot_surface(x, y, data)
    plt.title("Average Moves to the Kill Per " + str(steady_state) + " interations of training")

    if (gamma_range is not None) and (alpha_range is not None):
        plt.xlabel("Gamma")
        plt.ylabel("Alpha")
    elif (gamma_range is not None) and (epsilon_range is not None):
        plt.xlabel("Gamma")
        plt.ylabel("Epsilon")
    elif (alpha_range is not None) and (epsilon_range is not None):
        plt.xlabel("Alpha")
        plt.ylabel("Epsilon")

    plt.xlabel("Gamma")
    plt.ylabel("Epsilon")
    plt.savefig("Surface_Plot_"+str(steady_state))
    plt.show()

def plot_info(title_, x_axis, y_xis, x_data, y_data, save, display, labels = None):

    # generate plot
    for i in range(len(y_data)):
        plt.plot(x_data, y_data[i])

    if labels != None:
        for i in range(len(y_data)):
            plt.plot(x_data, y_data[i])
        plt.legend(labels)
    else:
        for i in range(len(y_data)):
            plt.plot(x_data, y_data[i])
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

    # vanilla plot
    simulations_per_training = 10
    max_training = 10**3
    info = average_moves_over_time(simulations_per_training, max_training,
                            epsilon = None, gamma = None, alpha = None, wolf_start = (0,0), grid_dim = 20, sheep_start = (19,19))
    plot_info("Average Moves Over time", "Number of Iterations", "Average Number of Moves",
              linspace(1,len(info),len(info)), [info], 0, 1)

    # a few plots of average moves per iteration trained for variable epsilon
    total_info = []
    epsilons = [.1 * i for i in range(11)]
    steady_state = 10*3
    averaging = 10
    x_values = [i for i in range(1,steady_state+1)]
    labels_ = ['epsilon = ' + str(ep) for ep in epsilons]
    for epsilon in epsilons:
        info = average_moves_over_time(averaging, steady_state,
                   epsilon=epsilon, gamma=None, alpha = None, wolf_start=(0, 0), grid_dim=20, sheep_start=(19, 19))
        total_info.append(info)
    plot_info("Average Moves Over time for Variable Epsilon", "Number of Iterations", "Average Number of Moves",
              x_values, total_info, 0, 1, labels = labels_)

    # a few plots of average moves per iteration trained for variable gamma
    total_info = []
    gammas = [.1 * i for i in range(11)]
    steady_state = 10*3
    averaging = 10
    x_values = [i for i in range(1,steady_state+1)]
    labels_ = ['gamma = ' + str(ep) for ep in gammas]
    for gamma in gammas:
        info = average_moves_over_time(averaging, steady_state,
                                       epsilon=None, gamma=gamma, alpha = None, wolf_start=(0, 0), grid_dim=20,
                                       sheep_start=(19, 19))
        total_info.append(info)
    plot_info("Average Moves Over Time for Variable Gamma", "Number of Iterations", "Average Number of Moves",
              x_values, total_info, 0, 1, labels = labels_)

    # a few plots of average moves per iteration trained for variable gamma
    total_info = []
    gammas = [.1 * i for i in range(11)]
    steady_state = 10*3
    averaging = 10
    x_values = [i for i in range(1,steady_state+1)]
    labels_ = ['gamma = ' + str(ep) for ep in gammas]
    for alpha in gammas:
        info = average_moves_over_time(averaging, steady_state,
                                       epsilon=None, gamma=None, alpha = alpha, wolf_start=(0, 0), grid_dim=20,
                                       sheep_start=(19, 19))
        total_info.append(info)
    plot_info("Average Moves Over Time for Variable Alpha", "Number of Iterations", "Average Number of Moves",
              x_values, total_info, 0, 1, labels = labels_)

    # now the surface plot of average moves at steady state for variable gamma and epsilon
    steady_state = 10**3 # number of training iterations (steady state)
    smoothness = 10 # how much averaging to do
    grid_spacing = 10*3 # number of evaluations for gamma and epsilon
    generate_surface_plots(steady_state, smoothness, grid_spacing, gamma_range=[0, 1], epsilon_range=[0, 1])
    generate_surface_plots(steady_state, smoothness, grid_spacing, gamma_range=[0, 1], alpha_range=[0, 1])
    generate_surface_plots(steady_state, smoothness, grid_spacing, epsilon_range=[0, 1], alpha_range=[0, 1])