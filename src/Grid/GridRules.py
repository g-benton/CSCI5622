"""Classes that execute certain actions based on whether certain conditions are
   met at each time step.
"""

import random

class SpawnNewActorRule:
    """Rule to spawn new Actor of given type in the grid."""

    def __init__(self, actor_name, actor_producer, actor_threshold=None,
                 time_interval=None):
        """Constructor. Can have one or both of the conditions, but not zero.
        Args:
            actor_name: The name of the type of actor to spawn.
            actor_producer: Function that takes in an actor id, init location
                and returns a valid Actor to add to the grid.
            actor_threshold: The amount of actor we should keep on the grid.
            time_interval: The time in between that we should spawn actor.
        """
        if actor_threshold is None and time_interval is None:
            raise ValueError('Need at least one condition.')
        self.actor_name = actor_name
        self.actor_producer = actor_producer
        self.actor_threshold = actor_threshold
        self.time_interval = time_interval
        self.time_counter = 0

    def update_if_valid(self, grid_world):
        """Update grid world if the conditions are met.
        Args:
            grid_world: The grid world object (not great have to pass this).
        Returns: True if the update happened.
        """
        # See if we should spawn an actor because of threshold requirement.
        if self.actor_threshold is not None:
            if (len(grid_world.observer.get_actor_type(self.actor_name))
                < self.actor_threshold):
                self._spawn_actor(grid_world)
                return True
        # See if we should span an actor because of time interval.
        if self.time_interval is not None:
            self.time_counter += 1
            if self.time_counter >= self.time_interval:
                self._spawn_actor(grid_world)
                self.time_counter = 0
                return True
        return False

    def _spawn_actor(self, grid_world):
        """Spawn the actor at a random location on the grid.
        Args:
            grid_world: The grid world object.
        """
        new_id = grid_world.largest_id + 1
        # Brute force this, keep coming up with new random position until
        # finally adds successfuly.
        x_dim, y_dim = grid_world.grid.grid_dim
        rand_location = (random.randint(0, x_dim - 1),
                         random.randint(0, y_dim - 1))
        actor = self.actor_producer(new_id, rand_location)
        while not grid_world.add_actor(actor, rand_location):
            rand_location = (random.randint(0, x_dim - 1),
                             random.randint(0, y_dim - 1))
            actor = self.actor_producer(new_id, rand_location)
