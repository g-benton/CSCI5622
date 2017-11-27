import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Prey(Actor):
    """A simple Prey class."""

    def __init__(self, actor_id, start_posn):
        self.prev_posn = None
        self.status = "ALIVE"
        super().__init__(actor_id, start_posn, PREY, False)

    def act(self, observer):
        """Give a next action.
        Args:
            observer: The GridObserver object (not needed for right now).
        Returns: Direction of next movement based on previous posn
        """

        # possible movements
        options = [NORTH, SOUTH, WEST, EAST]
        prob_wght = 0.1

        if(self.prev_posn is None):
            # random choice if first move
            return random.choice(options)
        else:
            # augment probabilities based on previous posn
            tuple_diff = tuple(np.subtract(self.posn, self.prev_posn))
            # tuple_diff = (0, 1)
            probs = [0.25 + prob_wght*tuple_diff[1],
                     0.25 - prob_wght*tuple_diff[1],
                     0.25 - prob_wght*tuple_diff[0],
                     0.25 + prob_wght*tuple_diff[0]]
            # print(probs)
            return np.random.choice(options, size=1, p=probs)[0]

    def update_posn(self, new_posn):
        """
        takes in tuple of next posn to move to
        updates the vars posn and prev_posn
        returns nothing
        """
        self.prev_posn = self.posn
        self.posn = new_posn

    def die(self):
        self.status = "DEAD"
