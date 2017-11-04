### external libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import ListedColormap
import sys
sys.path.append("../../Grid")

from GridConstants import *

# internal functions

class graph_vizualization:

    def __init__(self, start_grid_, frames_, interval_, location_info_):
        self.location_info = location_info_
        self.grid = start_grid_
        self.start_grid = list(start_grid_)
        self.frames = frames_
        self.interval = interval_
        self.frame = 0
        # print(self.location_info)

    # example updating function
    def update_grid(self, i):#, location_info, grid_mat):
        self._convert_to_np_array()
        self.draw_grid.set_array(self.grid)

        # if we've hit the frame limit stop updating
        if self.frame < self.frames:
            self.frame += 1

    def _convert_to_np_array(self):
        """ takes in dictionary of dictionaries of actor locations """
        self.grid = np.array(self.start_grid)
        # set up unique colors for the classes #
        colors = [i for i in range(1, len(self.location_info[0]) + 1)] # colors for the classes
        class_color_ind = -1 # colors indicator

        for location_dict, color in zip(self.location_info[self.frame].values(), colors):
            # class_color_ind += 1
            # color = colors[class_color_ind]
            for location in location_dict.values():
                self.grid[location[0], location[1]] = color


    def iterate(self):
        return None

    def display(self):
        fig, ax = plt.subplots()

        cmap = ListedColormap(['w', 'r', 'b', 'g', 'k'])
        self.draw_grid = ax.matshow(self.grid, cmap = cmap)
        # plt.colorbar(self.draw_grid)
        ani = animation.FuncAnimation(fig, self.update_grid, frames=self.frames, interval=self.interval)
        plt.show()


tester1 = {"wolf":{"1":(1,1), "2":(11,11)}, "sheep":{"3":(4,19),"4":(10, 15), "5":(12, 2)}}
tester2 = {"wolf":{"1":(1,2), "2":(12,11)}, "sheep":{"3":(5,19),"4":(11, 15), "5":(12, 1)}}
tester3 = {"wolf":{"1":(1,3), "2":(13,11)}, "sheep":{"3":(5,18),"4":(11, 14), "5":(11, 2)}}
# range(len(tester.values()))

tester = [tester1, tester2, tester3]

board_size = 20
grid_mat = np.array([[0.0 for i in range(board_size)] for k in range(board_size)])
grid_mat[:, 0] = BOARDER
grid_mat[:, board_size - 1] = BOARDER
grid_mat[0, :] = BOARDER
grid_mat[board_size - 1, :] = BOARDER

# M=np.array([[0,0,0,100,100,100,100,100,300,69,300,300,300,300,500,500,500,500,500,500,1000,1000,1000,1000] for i in range(0,20)])
# M=np.array([[0 for j in range(20)] for i in range(0,20)])

viz = graph_vizualization(start_grid_ = grid_mat, frames_ = len(tester), interval_ = 1000,
                          location_info_ = tester)
viz.display()
