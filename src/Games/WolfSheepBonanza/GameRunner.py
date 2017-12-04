"""Game under the scheme of having several sheep and several wolves. We run
the game for X steps and count how many sheep the wolves can catch in that
amount of time."""

import sys
import random
from matplotlib import pyplot as plt

from SmartPrey import SmartPrey
# from Predator import Predator

sys.path.append('../PredatorPreyBaseline')
from Predator import Predator as BaselinePredator

sys.path.append('../../Grid')
from GridConstants import *
from GridRules import SpawnNewActorRule
from GridWorld import GridWorld
from RunConditions import TimeLimitConditions


TIME_LIMIT = 100
SHEEP_NUM = 5
WOLF_NUM = 2
MAX_VISIBILITY = 10
GRID_SIZE = (25, 25)

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
    sheep_producer = lambda act_id, start_loc: SmartPrey(act_id, start_loc)
    spawn_sheep_rule = SpawnNewActorRule(PREY, sheep_producer,
                                         actor_threshold=SHEEP_NUM)
    world.add_rule(spawn_sheep_rule)
    return world

def train_wolves(save_q = False):
    pass

def evaluate(wolves, make_gif = False):
    """Evaluate any given wolf team.
    Args:
        wolves: List of predator objects.
        make_gif: Whether to display this evaluation in gif form.
    Returns: The number of sheep captured in the amount of time.
    """
    world = init_world(wolves)
    time_limit = TimeLimitConditions(TIME_LIMIT)
    world.run_simulation(time_limit, visualize=make_gif)
    return -1

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
    test_baseline(0, True)

if __name__ == '__main__':
    run()
