### external libraries
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# internal functions

class graph_vizualization:

    def __init__(self, start_grid_, frames_, interval_, location_info_):
        self.location_info = location_info_
        self.grid = np.array(start_grid_)
        self.frames = frames_
        self.interval = interval_
        # print(self.location_info)

    # example updating function
    def update_grid(self, i):#, location_info, grid_mat):
        self._convert_to_np_array()
        self.draw_grid.set_array(self.grid)


    def _convert_to_np_array(self):
        """ takes in dictionary of dictionaries of actor locations """

        # set up unique colors for the classes #
        # colors = [10*(i+1) for i in range( len( self.location_info.values() ) )]
        colors = [-0.1, 0.1]
        ind = -1
        for location_dict in self.location_info.values():
            ind += 1
            color = colors[ind]
            for location in location_dict.values():
                # print(color)
                self.grid[location[0], location[1]] = color
        # print(self.grid)

    # true updating function
    def iterate(self):
        return None

    def display(self):
        fig, ax = plt.subplots()
        self.draw_grid = ax.matshow(self.grid)
        # plt.colorbar(self.draw_grid)
        ani = animation.FuncAnimation(fig, self.update_grid, frames=self.frames, interval=self.interval)
        plt.show()


tester = {"wolf":{"1":(1,1), "2":(11,11)}, "sheep":{"3":(4,19),"4":(10, 15), "5":(12, 2)}}
# range(len(tester.values()))

grid_mat = np.array([[0.0 for i in range(20)] for k in range(20)])

# M=np.array([[0,0,0,100,100,100,100,100,300,69,300,300,300,300,500,500,500,500,500,500,1000,1000,1000,1000] for i in range(0,20)])
# M=np.array([[0 for j in range(20)] for i in range(0,20)])

viz = graph_vizualization(start_grid_ = grid_mat, frames_ = 30, interval_ = 500,
                          location_info_ = tester)
viz.display()
