import os
import sys
sys.path.append('../../Grid/')

os.chdir("/home/greg/Dropbox/CSCI5622/CSCI5622/src/Games/Hunter-Prey/")

import prey
import predator
import scratch_viz

board = np.array([[0 for j in range(20)] for i in range(0,20)])
viz = graph_vizualization(start_grid_ = M, frames_ = 30, interval_ = 500)
