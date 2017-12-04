import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class SmartPrey(Actor):
    """Prey that runs in the opposite direction of the closest Predator."""

    def __init__(self, actor_id, start_posn, grid_dim,
                 visibility = float('inf')):
        self.prev_posn = None
        self.grid_dim = grid_dim
        self.visibility = visibility
        super().__init__(actor_id, start_posn, PREY, False)

    def act(self, observer):
        """Give a next action.
        Args:
            observer: The GridObserver object (not needed for right now).
        Returns: Direction of next movement based on previous posn
        """
        closest_pred_loc = observer.get_closest(PREDATOR, self.posn)
        # IF there is no predator found or too far away make a random choice.
        if (closest_pred_loc is None
            or np.linalg.norm(closest_pred_loc, 2) > self.visibility):
            return random.choice([NORTH, WEST, EAST, SOUTH])

        # Make sorted list on what is the best option to pick. This heuristic
        # is based on moving away from the predator in the closest axis first
        # the the second axis, then moving towards in the second axis, then
        # lastly moving towards in the closest axis.
        x_dist = self.posn[0] - closest_pred_loc[0]
        y_dist = self.posn[1] - closest_pred_loc[1]
        best_actions = [NA, NA, NA, NA]
        if x_dist < 0:
            best_actions[0], best_actions[3] = WEST, EAST
        else:
            best_actions[0], best_actions[3] = EAST, WEST
        if y_dist < 0:
            best_actions[1], best_actions[2] = SOUTH, NORTH
        else:
            best_actions[1], best_actions[2] = NORTH, SOUTH
        if abs(x_dist) > abs(y_dist):
            best_actions[0], best_actions[1] = best_actions[1], best_actions[0]
            best_actions[2], best_actions[3] = best_actions[3], best_actions[2]

        # Try the actions in order until we have one where we don't run
        # into wall (note right now we don't consider other sheep.)
        for action in best_actions:
            if self._free_of_wall(action) and self._free_of_actor(action,
                                                                  observer):
                return action
        return NA

    def update_posn(self, new_posn):
        """
        takes in tuple of next posn to move to
        updates the vars posn and prev_posn
        returns nothing
        """
        self.prev_posn = self.posn
        self.posn = new_posn

    def _free_of_wall(self, action):
        """Check if we will run into a wall if we perform the given action.
        Args:
            action: The action to be performed.
        Returns: True if we can make the action without running into a wall,
            False otherwise.
        """
        if self.posn[0] == 0 and action == WEST:
            return False
        if self.posn[0] == self.grid_dim[0] - 1 and action == EAST:
            return False
        if self.posn[1] == 0 and action == SOUTH:
            return False
        if self.posn[1] == self.grid_dim[1] - 1 and action == NORTH:
            return False
        return True

    def _free_of_actor(self, action, observer):
        """Check if we will run into an actor if we perform the given action.
        Args:
            action: The action to be performed.
            observer: Grid Observer.
        Returns: True if we can make the action without running into an actor,
            False otherwise.
        """
        new_posn = self.posn
        if action == WEST:
            new_posn = (self.posn[0] - 1, self.posn[1])
        elif action == EAST:
            new_posn = (self.posn[0] + 1, self.posn[1])
        elif action == NORTH:
            new_posn = (self.posn[0], self.posn[1] + 1)
        elif action == SOUTH:
            new_posn = (self.posn[0], self.posn[1] - 1)
        return not observer.is_occupied(new_posn)
