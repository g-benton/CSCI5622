"""Gives information about the grid to the actor."""

class GridObserver:

    def __init__(self, grid):
        """Constructor.
        Args:
            grid: The Grid2D object.
        """
        self.grid = grid

    def get_actors(self):
        """Return the actors in the grid."""
        pass

    def get_location(self, actor_id):
        """Get the location of the actor."""
        pass

    def get_actor_type(self, name):
        """Get the all locations of actors with specified type.
        Returns: List of tuple locations (x, y).
        """
        pass

    def get_actors_in_posn(self, posn):
        """Get all of the actors in a position.
        Returns: List of actor objects.
        """
        pass
