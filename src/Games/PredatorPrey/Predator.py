import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Predator:
    """Simple Predator class."""

    def __init__(self, actor_id, start_posn):
        self.status = 'ALIVE'
        super().__init__(actor_id, start_posn, PREDATOR, False)

    def act(self):
        """
        returns direction of next movement based on previous location
        """

        #TODO: this is where the learning will take place !

    def die(self):
        self.status = "DEAD"
