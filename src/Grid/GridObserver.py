"""Gives information about the grid to the actor."""

import numpy as np

class GridObserver:

    def __init__(self, grid, actors):
        """Constructor.
        Args:
            grid: The Grid2D object.
            actors: Dictionary mapping actor name -> {id -> object}
        """
        self.grid = grid
        self.actors = actors

    def get_location(self, actor_id):
        """Get the location of the actor.
        Args:
            actor_id: The id of an actor.
        Returns: The tuple location (x, y) of the actor.
        """
        return self.grid.actor_to_posn[actor_id]

    def get_actor_type(self, name):
        """Get the all locations of actors with specified type.
        Args:
            name: The name of the actor (e.g. Prey, Predator).
        Returns: List of tuple locations (x, y).
        """
        ids = self.actors[name].keys()
        return [self.grid.actor_to_posn[i] for i in ids]

    def get_closest(self, name, posn):
        """Get the closest actor of specified type to the position.
        Args:
            name: The name of the type of object to get.
            posn: The (x, y) tuple position of where to look.
        Returns: The (x, y) tuple position of the closest actor.
        """
        ids = self.actors[name].keys()
        posns = [self.grid.actor_to_posn[i] for i in ids]
        dists = [(np.linalg.norm(np.subtract(posn, p)), p) for p in posns]
        dists.sort()
        if len(dists) == 0:
            return None
        return dists[0][1]

    def get_k_closest(self, name, posn, k):
        """Get the closest actor of specified type to the position.
        Args:
            name: The name of the type of object to get.
            posn: The (x, y) tuple position of where to look.
        Returns: The list (x, y) tuple position of the closest actor.
        """
        ids = self.actors[name].keys()
        posns = [self.grid.actor_to_posn[i] for i in ids]
        dists = [(np.linalg.norm(np.subtract(posn, p)), p) for p in posns]
        dists.sort()
        if len(dists) == 0:
            return None
        top_k = dists[:k]
        return [top_actor[1] for top_actor in top_k]

if __name__ == '__main__':

    dists = [0,1,2]
    top_k = dists[:1]
    print(top_k)