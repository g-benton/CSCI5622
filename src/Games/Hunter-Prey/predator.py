import random
import numpy as np

UP = "UP"
DOWN = "DOWN"
LEFT = "LEFT"
RIGHT = "RIGHT"

class predator:
    """ simple wolf class """

    def __init__(self, location, pred_id):

        self.location = (location[0], location[1])
        self.prev_location = None
        self.id = pred_id
        self.status = "ALIVE"

    def act(self):
        """
        returns direction of next movement based on previous location
        """

        #TODO: this is where the learning will take place !


    def update_location(self, new_location):
        """
        takes in tuple of next location to move to
        updates the vars location and prev_location
        returns nothing
        """

        self.prev_location = self.location
        self.location = new_location

    def die(self):
        self.status = "DEAD"
