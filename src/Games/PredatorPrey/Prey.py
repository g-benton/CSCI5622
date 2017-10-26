
import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Prey(Actor):
    """A simple Prey class."""

    def __init__(self, actor_id, start_posn):
        self.prev_location = None
        self.status = "ALIVE"
        super().__init__(actor_id, start_posn, PREY, True)

    def act(self):
        """
        returns direction of next movement based on previous location
        """

        # possible movements
        options = [NORTH, SOUTH, WEST, EAST]
        prob_wght = 0.2

        if(self.prev_location is None):
            # random choice if first move
            return random.choice(options)
        else:
            # augment probabilities based on previous location
            tuple_diff = tuple(np.subtract(self.location, self.prev_location))
            tuple_diff = (0, 1)
            probs = [0.25 + prob_wght*tuple_diff[1],
                     0.25 - prob_wght*tuple_diff[1],
                     0.25 - prob_wght*tuple_diff[0],
                     0.25 + prob_wght*tuple_diff[0]]

            return random.choices(options, size=1, p=probs)[0]

    def update_posn(self, new_location):
        """
        takes in tuple of next location to move to
        updates the vars location and prev_location
        returns nothing
        """
        self.prev_location = self.posn
        self.posn = new_location

    def die(self):
        self.status = "DEAD"
