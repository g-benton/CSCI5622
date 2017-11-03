"""Superclass for all agents/npcs to extend from."""

from GridConstants import NA

class Actor:

    def __init__(self, actor_id, start_posn, name, can_overlap):
        """Constructor.
        Args:
            actor_id: The unique identifying ID of the actor.
            start_posn: Tuple of the start position (x, y)
            name: The name of the actor as a string, e.g. "Predator".
            can_overlap: Whether the actor can be overlapped on the grid.
        """
        self.actor_id = actor_id
        self.posn = start_posn
        self.name = name
        self.can_overlap = can_overlap

    def act(self):
        """Method that makes the actor act, does nothing here, should be
        implemented in subclasses.
        Returns: No Action constant.
        """
        return NA

    def update_posn(self, posn):
        """Updates the actors position.
        Args:
            posn: The new position that we have moved to.
        """
        self.posn = posn

    # TODO: Figure out best way to give feedback to actors.
    def get_feedback(self, feedback):
        """Give feedback to the actor, does nothing here, should be implemented
        in subclasses.
        Args:
            feedback: TBD
        """
        pass

    def get_actor_id(self):
        """Returns the actor id."""
        return self.actor_id

    def get_name(self):
        """Returns the name."""
        return self.name

    def get_can_overlap(self):
        """Returns whether agent can be overlapped."""
        return self.can_overlap

    def get_posn(self):
        """Returns the position."""
        return self.posn
