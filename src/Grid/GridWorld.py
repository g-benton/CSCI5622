"""Class that runs the Grid simulation. Makes agent act, updates agents/reward,
and updates the grid.
"""

import copy

from Grid2D import Grid2D
from GridObserver import GridObserver
from GridVisualizer import GridVisualizer
from GridConstants import *

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
        # List of actions to take given certain conditions are met at time step.
        self.rules = []
        # Set of actor ids that we have seen.
        self.seen_ids = set()
        # Largest actor id that we have seen.
        self.largest_id = -1
        # include number of moves in game
        self.moves_in_game = 0

    def add_actor(self, actor, start_position):
        """Add actor to our GridWorld.
        Args:
            actor: Actor object we wish to add to game world.
            start_position: The starting position on the grid as Tuple (x, y).
        Returns: True or False if we were able to successfuly add the actor.
        """
        if actor.actor_id in self.seen_ids:
            raise ValueError('Non-unique actor id')
        if actor.name not in self.actors:
            self.actors[actor.get_name()] = {}
        if not self.grid.add_actor(actor, start_position):
            return False
        self.actors[actor.name][actor.get_actor_id()] = actor
        self.seen_ids.add(actor.actor_id)
        if actor.actor_id > self.largest_id:
            self.largest_id = actor.actor_id
        return True

    def add_rule(self, rule):
        """Add a rule to world.
        Args:
            rule: A Rule object.
        """
        self.rules.append(rule)

    def run_simulation(self, condition, visualize=False, overlap_tracker=None):
        """Runs the simulations while the condtion is true.
        Args:
            condition: Condition object that tells how long to train.
            visualize: Whether to visualize the output.
            overlap_tracker: Tracker object to track num prey captured.
        """
        # TODO: Figure out what info should be passed to condition, none needed
        # for now.
        if visualize:
            history = []
        while condition.is_running(self.observer):
            self._step(overlap_tracker)
            if visualize:
                history.append(self._history_snapshot())
        # The simulation has ended, now simulate!
        if visualize:
            viz = GridVisualizer(self.grid.grid_dim[0], len(history) - 1,
                                 VIZ_SPEED, history)
            viz.display()

    def _step(self, overlap_tracker=None):
        """Do one time step in our simulation.
        Args:
            overlap_tracker: Tracker object to track num prey captured.
        """
        # update number of moves
        self.moves_in_game += 1
        # Have all the actors propose actions.
        id_to_action = {}
        for actor_type in self.actors.keys():
            for actor in self.actors[actor_type].values():
                id_to_action[actor.actor_id] = actor.act(self.observer)
        # Have actors try to take those actions.
        for actor_type in self.actors.keys():
            for actor in self.actors[actor_type].values():
                action = id_to_action[actor.actor_id]
                new_posn = self.grid.move_actor(actor, action)
                actor.update_posn(new_posn)
        # Have all actors get feeback on their actions.
        for actor_type in self.actors.keys():
            for actor in self.actors[actor_type].values():
                actor.give_feedback(self.observer)
        # Remove the actors that have been overlapped.
        removed = self.grid.remove_overlapped()
        if overlap_tracker is not None:
            overlap_tracker.add(len(removed))
        for rem in removed:
            for actor_dic in self.actors.values():
                if rem in actor_dic:
                    del actor_dic[rem]
        # Execute the rules.
        for rule in self.rules:
            rule.update_if_valid(self)

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

    def _number_of_moves(self):
        return self.moves_in_game
