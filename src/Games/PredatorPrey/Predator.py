import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Predator(Actor):
    """Simple Predator class."""

    def __init__(self, actor_id, start_posn, dim, epsilon = None):

        super().__init__(actor_id, start_posn, PREDATOR, True)

        # q_mat has (2n-1)^2 + 1 rows and 5 columns, since there are (2n-1)^2
        # different states (+1 is for the situation where there is no sheep)
        # and 5 different actions for the actor to take
        self.q_mat = np.matrix(((2*(dim-1))**2 + 1)*[5*[0]])
        # initialize epsilon
        if epsilon is None:
            self.epsilon = 1.0
        else:
            self.epsilon = epsilon

        self.actions = [NORTH,SOUTH,EAST,WEST,NA]
        self.dim = dim
        self.prev_state = int(-1)
        self.alpha = 0.1
        self.gamma = 0.8

    def get_state(self,observer):
        """
        :param observer: the observer class
        :return: the index in the Q matrix that corresponds to the state of the predator. Note that the index for the
         q-matrix is the distance vector from base (2*dim - 1) to base 10
        """
        closest_sheep = observer.get_closest(PREY, self.posn)
        if closest_sheep is None:
            return int(-1) # so the state goes to the last row of Q
        else:
            distance = np.linalg.norm(np.subtract(self.posn, closest_sheep), ord=1)
            distance = np.add(distance, (self.dim - 1, self.dim - 1))
            return int(np.floor(distance[1] / float(2 * self.dim - 1)) + distance[0] % float(2 * self.dim - 1))

    def act(self, observer):
        state = self.get_state(observer)
        q = self.q_mat[int(state),:].tolist()[0]
        if random.random() < self.epsilon:
            if sum(q) == 0:
                probs = [1.0/len(q) for i in q]
            else:
                sum_q = sum(q)
                probs = [float(i)/sum_q for i in q]
            action_ind = np.random.choice(range(len(q)), p = np.array(probs))
        else:
            max_q = max(q)
            maxes = [i for i, x in enumerate(q) if x == max_q]
            action_ind = np.random.choice(maxes)
        self.prev_state = int(state)
        return self.actions[action_ind]

    def give_feedback(self, observer):
        """
        :param observer: the observer class
        :return: nada - just updates the Q matrix
        """
        state = self.get_state(observer)

        if state == ((2*self.dim-1)^2-1)/2:
            r = 1000.0
            self.epsilon *= 0.99
        else:
            r = 0.0

        self.q_mat[self.prev_state] = (1-self.alpha)*self.q_mat[self.prev_state] + \
                                      self.alpha*(r + self.gamma*max(self.q_mat[state]))

    def write_q(self,outfile):
        np.save(outfile, self.q_mat)

    def read_q(self,outfile):
        self.q_mat = np.load(outfile)

if __name__ == '__main__':
    pass