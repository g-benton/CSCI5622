"""Class that handles 2D Grid Information and Placement of Agnets."""

from GridConstants import *

class Grid2D:

    def __init__(self, grid_dim):
        """Constructor
        Args:
            grid_dim: Tuple (x, y) of the size of the grid.
        """
        self.grid_dim = grid_dim
        # Maps actor's unique ID to location on the grid.
        self.actor_to_posn = {}
        # Maps tuple position to a list of actor objects.
        self.posn_to_actor = {}

    def add_actor(self, actor, start_position):
        """Adds an actor onto the grid at the start position.
        Args:
            actor: Either Agent or NPC type object, needs actor_id.
            start_position: Tuple of the location (x, y).
        Returns: True if we succesfully added Agent, False otherwise.
        """
        if not actor.get_can_overlap():
            if start_position in self.posn_to_actor:
                return False
        self._update_actor_posn(actor, start_position)
        return True

    def move_actor(self, actor, action):
        """Move actor in the grid.
        Args:
            actor: The actor to be moved.
            action: The action for the actor to take.
        Returns: The new position that the actor ended up at and the ids of the
            actors at the new location.
        """
        curr_posn = self.actor_to_posn[actor.get_actor_id()]
        new_posn = self._get_new_posn(curr_posn, action)
        if not actor.get_can_overlap(): # prey tries to move to occupied space
            if new_posn in self.posn_to_actor:
                return curr_posn
        if new_posn is not None: # predator is moving onto occupied space
            # TODO: validate movement based on predator consuming prey
            new_posn = self.check_movement_overlap(actor = actor,
                                                   new_posn = new_posn)
            self._update_actor_posn(actor, new_posn, curr_posn)
        if new_posn is None: # thing doesn't move
            new_posn = curr_posn
        return new_posn

    def check_movement_overlap(self, actor, new_posn):
        """
        Checks movements to determine if a predator is moving onto a prey
        or if a prey is attempting to move onto an occupied space
        """
        if actor.can_overlap:
            # print(self.posn_to_actor[new_posn])
            # predator class #
            if new_posn in self.posn_to_actor:
                for actor in self.posn_to_actor[new_posn]:
                    if actor.can_overlap:
                        pred_in_new_posn = True

                if pred_in_new_posn:
                    # can't move into new space #
                    new_posn = None
        return new_posn

    def remove_overlapped(self):
        """Remove any actors that are overlapped.
        Returns: List of actor ids that have been overlapped.
        """
        removed = []
        for actors in self.posn_to_actor.values():
            if len(actors) > 1:
                for actor in actors:
                    if not actor.get_can_overlap():
                        a_id = actor.get_actor_id()
                        self._remove_actor(a_id)
                        removed.append(a_id)
        return removed

    def _remove_actor(self, actor_id):
        """Remove an actor from the grid.
        Args:
            actor_id: The id of the actor to be removed.
        Returns: True if able to remove the actor.
        """
        if actor_id not in self.actor_to_posn:
            return False
        actor_posn = self.actor_to_posn[actor_id]
        del self.actor_to_posn[actor_id]
        self.posn_to_actor[actor_posn].remove(actor_id)

    def _update_actor_posn(self, actor, new_posn, old_posn=None):
        """Update the actor's position on the Grid.
        Args:
            actor: The actor to be updated.
            new_posn: The position the actor should be moved to.
            old_posn: Where the actor just was, if old_posn is none do not
                erase history (i.e. don't want this if adding to grid for
                first time.
        """
        if self._is_valid_posn(new_posn):
            self.actor_to_posn[actor.get_actor_id()] = new_posn
            # Add to new position.
            if new_posn not in self.posn_to_actor:
                self.posn_to_actor[new_posn] = []
            self.posn_to_actor[new_posn].append(actor)
            # Remove from old position.
            if old_posn is not None:
                self.posn_to_actor[old_posn].remove(actor)
                # If there are no longer any actors in that position delte.
                if len(self.posn_to_actor[old_posn]) == 0:
                    del self.posn_to_actor[old_posn]

    def _get_new_posn(self, curr_posn, action):
        """Return a new position based on the action taken.
        Args:
            curr_posn: Current position on the grid
            action: The action that the actor will take.
        Returns: Tuple (x, y) of the new location, or None if location is off
        the grid or if given invalid action.
        """
        new_posn = (-1, -1)
        if action == NORTH:
            new_posn = (curr_posn[0], curr_posn[1] + 1)
        elif action == SOUTH:
            new_posn = (curr_posn[0], curr_posn[1] - 1)
        elif action == WEST:
            new_posn = (curr_posn[0] - 1, curr_posn[1])
        elif action == EAST:
            new_posn = (curr_posn[0] + 1, curr_posn[1])
        elif action == NA:
            new_posn = curr_posn
        # Check if we went out of bounds of the grid, if so return None.
        if not self._is_valid_posn(new_posn):
            return None
        return new_posn

    def _is_valid_posn(self, posn):
        """Check if the position is a valid position on the grid.
        Args:
            posn: The position to check.
        Returns: True of False.
        """
        if posn[0] < 0 or posn[0] >= self.grid_dim[0]:
            return False
        if posn[1] < 0 or posn[1] >= self.grid_dim[1]:
            return False
        return True
