import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Obstacle(Actor):
    """Simple Predator class."""

    def __init__(self, actor_id, start_posn, dim, epsilon = None):

        super().__init__(actor_id, start_posn, OBSTACLE, True)
        self.actions = [NA]
        self.dim = dim
        self.prev_state = int(-1)
        self.prev_action = int(-1)
        self.moves = 0

    def get_state(self,observer):
        """
        Not currently any use for this function
        """
        return 0

    def act(self, observer):
        """
        Not currently any use for this function
        """
        return NA


if __name__ == '__main__':
    test = np.mat([[1,2,3],[2,3,4]])
    print(test[1].max())
    test[1] = (1-0.1)*test[0] + 0.1*(0.8*(test[1].max()))
    print(test)