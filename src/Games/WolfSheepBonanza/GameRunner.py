"""Game under the scheme of having several sheep and several wolves. We run
the game for X steps and count how many sheep the wolves can catch in that
amount of time."""

import sys
import random
from matplotlib import pyplot as plt

from SmartPrey import SmartPrey

sys.path.append('../PredatorPreyMultiSheep')
from Predator import Predator

sys.path.append('../PredatorPreyBaseline')
from BaselinePredator import Predator as BaselinePredator

sys.path.append('../../Grid')
from GridConstants import *
from GridRules import SpawnNewActorRule
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions
from OverlapTracker import OverlapTracker


TIME_LIMIT = 1000
SHEEP_NUM = 3
WOLF_NUM = 2
MAX_VISIBILITY = 10
GRID_SIZE = (10,10)

# Learning Parameters
# learning rate (consider how random the process is)
ALPHA = 0.01
# percent propogated back in Q-matrix equation (consider size of state space)
GAMMA = 0.8
# percentage of time spent exploring
EPSILON = 0.25
# decay of epsilon each time the sheep is killed
EPSILON_DECAY = 0.01
# lower bound for epsilon
MIN_EPS = 0.001
# Fraction of reward that should be used as penalty if the wolf makes no capture
RHO = 0.2

def init_world(wolves):
    """Initialize the world ready to run.
    Args:
        wolves: List of wolf objects to insert into the game.
    Returns: Game object ready to be run.
    """
    world = GridWorld(GRID_SIZE)
    for wolf in wolves:
        world.add_actor(wolf, wolf.posn)
    # Anonymous function that tells us how to make new sheep.
    sheep_producer = lambda act_id, start_loc: SmartPrey(act_id, start_loc,
                                                         GRID_SIZE,
                                                         visibility = 10)
    spawn_sheep_rule = SpawnNewActorRule(PREY, sheep_producer,
                                         actor_threshold=SHEEP_NUM)
    world.add_rule(spawn_sheep_rule)
    return world

def train_wolves(episodes, make_gif = True, save_q=False):
    """Train a set of wolves.
    Args:
        episodes: The number of games the wolves should play for training.
        make_gif: Whether a gif should be made of the final product.
        save_q: Whether the q_matrix should be saved.
    Returns: List of scores.
    """
    # Init the wolves.
    wolves = []
    start_posns = get_random_posns(WOLF_NUM)
    for actor_id in range(WOLF_NUM):
        wolf = Predator(actor_id, start_posns[actor_id],
                        [[1,3,5,100]],[[-120, -60, 0, 60, 120]], # predator info
                        [[1,3,5,100] for _ in range(3)],
                        [[-120, -60, 0, 60, 120] for _ in range(3)], # prey info
                        [[]],[[]], # obstacle info
                        [[]], # wall info
                        alpha=ALPHA, gamma=GAMMA, epsilon=EPSILON,
                        epsilon_decay_per_epoch=EPSILON_DECAY,
                        penalty_fraction=RHO,
                        min_epsilon=MIN_EPS)
        wolves.append(wolf)

    # Train the wolves.
    scores = []
    for ep in range(episodes):
        score = evaluate(wolves)
        scores.append(score)
        if ep > 10:
            roll_avg = sum(scores[-10:])/len(scores[-10:])
            print('Finished episode %d w/ score %d, rolling average %f'\
                 % (ep + 1, score, roll_avg))
        else:
            print('Finished episode %d w/ score %d'\
                 % (ep + 1, score) )
    if make_gif:
        evaluate(wolves, make_gif)
    return scores

def evaluate(wolves, make_gif = False):
    """Evaluate any given wolf team.
    Args:
        wolves: List of predator objects.
        make_gif: Whether to display this evaluation in gif form.
    Returns: The number of sheep captured in the amount of time.
    """
    world = init_world(wolves)
    time_limit = TimeLimitConditions(TIME_LIMIT)
    tracker = OverlapTracker()
    world.run_simulation(time_limit, visualize=make_gif, overlap_tracker=tracker)
    return tracker.get_num_overlaps()

def test_baseline(num_sims, make_gif = False):
    """Test the world with the baseline wolves.
    Args:
        num_sims: Number of times to run the simulation.
        make_gif: Whether to display the final evaluation with a gif.
    Returns: List of how many sheep were captured in each game.
    """
    actor_id = 0
    baseline_wolves = []
    start_posns = get_random_posns(WOLF_NUM)
    for i in range(WOLF_NUM):
        baseline_wolves.append(BaselinePredator(actor_id, start_posns[actor_id],
                                                GRID_SIZE,
                                                visibility = MAX_VISIBILITY))
        actor_id += 1
    scores = [evaluate(baseline_wolves) for _ in range(num_sims)]
    if make_gif:
        evaluate(baseline_wolves, make_gif)
    return scores

def get_random_posns(num_posns):
    """Get unique, random positions in the grid.
    Args:
        num_posns: The number of unique positions.
    Returns: List of start positions as tuples.
    """
    seen = set()
    while len(seen) < num_posns:
        posn = (random.randint(0, GRID_SIZE[0] - 1),
                random.randint(0, GRID_SIZE[1] - 1))
        seen.add(posn)
    return list(seen)

def run():
    # baselines = test_baseline(0, True)
    # print(sum(baselines) / len(baselines))
    # print(max(baselines))
    # print(min(baselines))
    trained_scores = train_wolves(10000)
    print(sum(trained_scores) / len(trained_scores))
    print(max(trained_scores))
    print(min(trained_scores))

if __name__ == '__main__':
    run()
