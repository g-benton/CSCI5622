### external libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import copy
import sys
sys.path.append("../../Grid")

from GridConstants import *

# internal functions

class GridVisualizer:

    def __init__(self, board_size_, frames_, interval_, location_info_):
        start_grid = ( np.array([[0 for i in range(board_size_)]
                                    for k in range(board_size_)]) )

        # set up an init grid that will cover the number of actor types (for coloring)
        # init_grid = start_grid
        init_grid = copy.deepcopy(start_grid)
        for col_ind in range(MAX_ACTOR_TYPES):
            init_grid[0, col_ind] = col_ind

        self.location_info = location_info_
        self.grid = init_grid
        self.start_grid = list(start_grid)
        self.frames = frames_
        self.interval = interval_
        self.frame = 0

    # example updating function
    def update_grid(self, i):#, location_info, grid_mat):
        self._convert_to_np_array()
        self.draw_grid.set_array(self.grid)

        # if we've hit the frame limit stop updating
        if self.frame < self.frames:
            self.frame += 1
        else:
            self.frame = 0

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
        values = [1,2]
        labels = list(self.location_info[0].keys())
        cmap = ListedColormap(['w', 'r', 'b', 'g', 'k'])
        self.draw_grid = ax.matshow(self.grid, cmap = cmap)
        colors = [ self.draw_grid.cmap(self.draw_grid.norm(value)) for value in values]
        # create a patch (proxy artist) for every color
        patches = [ mpatches.Patch(color=colors[i], label= labels[i]) for i in range(len(values)) ]
        # put those patched as legend-handles into the legend
        plt.legend(handles=patches, bbox_to_anchor=(0.5, -0.05), loc=9, borderaxespad=0., ncol = 2)

        ani = animation.FuncAnimation(fig, self.update_grid, frames=self.frames, interval=self.interval)
        # plt.legend(['predator', 'prey'], loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
        plt.show()


if __name__ == '__main__':
    board_size = 20

    tester1 = {"wolf":{"1":(1,1), "2":(11,11)}, "sheep":{"3":(4,19),"4":(10, 15), "5":(12, 2)}}
    tester2 = {"wolf":{"1":(1,2), "2":(12,11)}, "sheep":{"3":(5,19),"4":(11, 15), "5":(12, 1)}}
    tester3 = {"wolf":{"1":(1,3), "2":(13,11)}, "sheep":{"3":(5,18),"4":(11, 14), "5":(11, 2)}}
    tester = [tester1, tester2, tester3]


    viz = GridVisualizer(board_size_ = board_size, frames_ = len(tester) - 1,
                            location_info_= tester, interval_= 10)
    viz.display()
