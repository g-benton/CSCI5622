
import random
import numpy as np

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

class prey:
    """ simple sheep class """

    def __init__(self, location):

        self.location = (location[0], location[1])
        self.prev_location = None
        self.status = "ALIVE"

    def act():
        """
        returns direction of next movement based on previous location
        """

        # possible movements
        options = [UP, DOWN, LEFT, RIGHT]
        prob_wght = 0.2

        if(self.prev_location is None):
            # random choice if first move
            return random.choice(options)
        else:
            # augment probabilities based on previous location
            tuple_diff = tuple( np.subtract(self.location, self.prev_location) )
            tuple_diff = (0, 1)
            probs = [0.25 + prob_wght*tuple_diff[1], 0.25 - prob_wght*tuple_diff[1],
                     0.25 - prob_wght*tuple_diff[0], 0.25 + prob_wght*tuple_diff[0]]

            return( random.choices(options, size = 1, p = probs)[0] )


    def update_location(new_location):
        """
        takes in tuple of next location to move to
        updates the vars location and prev_location
        returns nothing
        """

        self.prev_location = self.location
        self.location = new_location

        return None
