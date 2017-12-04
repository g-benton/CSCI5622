import random
import numpy as np
import random

import sys
sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Predator(Actor):
    """Simple Predator class."""

    def __init__(self, actor_id, start_posn, dim, epsilon = None,
                 visibility = float('inf')):
        """Constructor:
        Args:
            visibility: How far the predator can see in the 2-norm.
        """
        super().__init__(actor_id, start_posn, PREDATOR, True)
        self.moves = 0
        self.visibility = visibility

    def act(self, observer):

        # get the location of the closest sheep
        closest_sheep = observer.get_closest(PREY, self.posn)

        # don't move if there is no sheep
        if closest_sheep is None:
            return NA

        # if there is a sheep, find the distance to the closest one
        distance = np.subtract(closest_sheep, self.posn)
        abs_distance = np.absolute(distance)
        max_index = abs_distance.tolist().index(max(abs_distance))

        # If the sheep is too far away for us to see, choose a random direction.
        if np.linalg.norm(distance, 2) > self.visibility:
            return random.choice([NORTH, EAST, WEST, SOUTH])

        if distance[max_index] > 0:
            if max_index == 0:
                return EAST
            else:
                return NORTH

        elif distance[max_index] < 0:
            if max_index == 0:
                return WEST
            else:
                return SOUTH

        else:
            return NA

        # update the number of moves that the predetor has used
        self.moves += 1

if __name__ == '__main__':
    test = np.mat([[1,2,3],[2,3,4]])
    print(test[1].max())
    test[1] = (1-0.1)*test[0] + 0.1*(0.8*(test[1].max()))
    print(test)
