"""Class that runs the Grid simulation. Makes agent act, updates agents/reward,
and updates the grid.
"""

from Grid2D import Grid2D
from GridObserver import GridObserver

class GridWorld:

    def __init__(self, grid_dim, actor_precedences):
        """Constructor.
        Args:
            grid_dim: Tuple of the grid size (x, y).
            actor_precedences: List of the actor names so we know precedences
                of which actors go first on discrete time step.
        """
        self.grid = Grid2D(grid_dim)
        # Map actor name -> {actor id -> actor object}.
        self.actors = {}
        self.observer = GridObserver(self.grid, self.actors)
        self.actor_precedences = actor_precedences

    def add_actor(self, actor, start_position):
        """Add actor to our GridWorld.
        Args:
            actor: Actor object we wish to add to game world.
            start_position: The starting position on the grid as Tuple (x, y).
        """
        if actor.name not in self.actors:
            self.actors[actor.get_name()] = {}
        self.actors[actor.name][actor.get_actor_id()] = actor
        self.grid.add_actor(actor, start_position)

    def remove_actor(self, actor_name, actor_id):
        """Remove an actor given their name and id.
        Args:
            actor_name: The name of the actor type.
            actor_id: The id of the actor to remove.
        """
        self.grid.remove_actor(actor_id)
        del self.actors[actor_name][actor_id]

    def run_simulation(self, condition):
        """Runs the simulations while the condtion is true."""
        # TODO: Figure out what info should be passed to condition, none needed
        # for now.
        while condition.is_running(None):
            self._step()

    def _step(self):
        """Do one time step in our simulation."""
        for actor_type in self.actor_precedences:
            for actor in self.actors[actor_type].values():
                action = actor.act(self.observer)
                new_posn = self.grid.move_actor(actor, action)
                actor.update_posn(new_posn)
                # Give actor feedback here.
