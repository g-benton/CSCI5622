from GridConstants import *

"""Different classes for conditions of how long to run the games."""

class TimeLimitConditions:

    def __init__(self, step_limit):
        """Constructor:
        Args:
            step_limit: The number of steps for the simulation to run for.
        """
        self.step_limit = step_limit

    def is_running(self, grid_info):
        """Tells whether the game is still running.
        Args:
            grid_info: Not used here.
        Returns: True if the game should keep running, False otherwise.
        """
        self.step_limit -= 1
        return self.step_limit >= 0


class NoPreyConditions:

    def is_running(self, grid_info):
        """
        Tells whether the game is still running.
        based on whether there are any prey left in the simulation
        """
        ### grid info will be of the class Grid Observer ###

        # get out the list of prey actors in the sim
        prey_actors = grid_info.get_actor_type(PREY)

        # if there aren't any left then kill the sim #
        if len(prey_actors) == 0:
            return False
        else:
            return True


class CombinedConditions:

    def __init__(self, step_limit):
        self.step_limit = step_limit

    def is_running(self, grid_info):

        self.step_limit -= 1
        prey_actors = grid_info.get_actor_type(PREY)

        if len(prey_actors) == 0 or self.step_limit < 0:
            return False
        else:
            return True
