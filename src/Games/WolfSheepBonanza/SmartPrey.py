import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class SmartPrey(Actor):
    """Prey that runs in the opposite direction of the closest Predator."""

    def __init__(self, actor_id, start_posn):
        self.prev_posn = None
        super().__init__(actor_id, start_posn, PREY, False)

    def act(self, observer):
        """Give a next action.
        Args:
            observer: The GridObserver object (not needed for right now).
        Returns: Direction of next movement based on previous posn
        """
        closest_pred_loc = observer.get_closest(PREDATOR, self.posn)
        x_dist = self.posn[0] - closest_pred_loc[0]
        y_dist = self.posn[1] - closest_pred_loc[1]
        if abs(x_dist) < abs(y_dist):
            if x_dist > 0:
                return WEST
            else:
                return EAST
        else:
            if y_dist > 0:
                return NORTH
            else:
                return SOUTH

    def update_posn(self, new_posn):
        """
        takes in tuple of next posn to move to
        updates the vars posn and prev_posn
        returns nothing
        """
        self.prev_posn = self.posn
        self.posn = new_posn
