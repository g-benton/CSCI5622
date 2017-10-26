"""Class that runs the Grid simulation. Makes agent act, updates agents/reward,
and updates the grid.
"""

class GridWorld:

    def __init__(self, grid_dim):
        self.grid = Grid(grid_dim)
        self.agents = []
        self.npcs = []

    def add_agent(self, agent, start_position):
        self.agents.append(agent)
        self.grid.add_actor(agent, start_position)

    def add_npc(self, npc, start_position):
        self.npcs.append(npc)
        self.grid.add_actor(npc, start_position)

    def remove_agent(self, agent):
        self.agents.remove(agent)

    def remove_npc(self, npc):
        self.npc.remove(npc)

    def run_simulation(self, condition):
        """Runs the simulations while the condtion is true."""
        while condition():
            for agent in self.agents:
                action = agent.act()
                new_posn = self.grid.update_position(agent, action)
                agent.update_position(new_posn)
                # Give feeback about the reward stuff here.
            for npc in self.npcs:
                action = npc.act()
                new_posn = self.grid.update_position(npc, action)
                npc.update_position(new_posn)

