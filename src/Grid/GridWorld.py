"""Class that runs the Grid simulation. Makes agent act, updates agents/reward,
and updates the grid.
"""

import copy

from Grid2D import Grid2D
from GridObserver import GridObserver
from GridVisualizer import GridVisualizer

class GridWorld:

    def __init__(self, grid_dim):
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

    def run_simulation(self, condition, visualize=False):
        """Runs the simulations while the condtion is true.
        Args:
            condition: Condition object that tells how long to train.
            visualize: Whether to visualize the output.
        """
        # TODO: Figure out what info should be passed to condition, none needed
        # for now.
        if visualize:
            history = []
        while condition.is_running(None):
            self._step()
            if visualize:
                history.append(self._history_snapshot())
        # The simulation has ended, now simulate!
        if visualize:
            viz = GridVisualizer(self.grid.grid_dim[0], len(history) - 1,
                                 1000, history)
            viz.display()

    def _step(self):
        """Do one time step in our simulation."""
        # Have all the actors act.
        for actor_type in self.actors.keys():
            for actor in self.actors[actor_type].values():
                action = actor.act(self.observer)
                new_posn = self.grid.move_actor(actor, action)
                actor.update_posn(new_posn)
        # Have all actors get feeback on their actions.
        for actor_type in self.actors.keys():
            for actor in self.actors[actor_type].values():
                actor.give_feedback(self.observer)
        # Remove the actors that have been overlapped.
        removed = self.grid.remove_overlapped()
        for rem in removed:
            for actor_dic in self.actors.values():
                if rem in actor_dic:
                    del actor_dic[rem]


    def _history_snapshot(self):
        """Take a snapshot of the current state of the actors with their posns.
        Returns: Dict name -> {id -> (x, y)}
        """
        snapshot = {}
        for name, inner in self.actors.items():
            snapshot[name] = {}
            for actor_id, actor in inner.items():
                snapshot[name][actor_id] = actor.posn
        return snapshot
