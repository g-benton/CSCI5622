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
