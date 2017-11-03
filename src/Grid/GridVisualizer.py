### external libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# internal functions

class graph_vizualization:

    def __init__(self, start_grid_, frames_, interval_):
        self.grid = np.array(start_grid_)
        self.frames = frames_
        self.interval = interval_

    # example updating function
    def update_grid(self,i):
        M[7, i] = 1000
        M[19 - i, 10] = 500
        self.draw_grid.set_array(M)

    # true updating function
    def iterate(self):
        return None

    def display(self):
        fig, ax = plt.subplots()
        self.draw_grid = ax.matshow(self.grid)
        # plt.colorbar(self.draw_grid)
        ani = animation.FuncAnimation(fig, self.update_grid, frames=self.frames, interval=self.interval)
        plt.show()


# M=np.array([[0,0,0,100,100,100,100,100,300,69,300,300,300,300,500,500,500,500,500,500,1000,1000,1000,1000] for i in range(0,20)])
# M=np.array([[0 for j in range(20)] for i in range(0,20)])
#
#
# viz = graph_vizualization(start_grid_ = M, frames_ = 30, interval_ = 500)
# viz.display()
