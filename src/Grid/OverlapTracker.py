class OverlapTracker:
    """Tracks how many overlaps are in a game."""

    def __init__(self):
        """Constructor."""
        self.num_overlaps = 0

    def add(self, new_overlaps):
        self.num_overlaps += new_overlaps

    def get_num_overlaps(self):
        return self.num_overlaps
