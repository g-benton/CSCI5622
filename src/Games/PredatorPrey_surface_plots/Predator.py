import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Predator(Actor):
    """Simple Predator class."""

    def __init__(self, actor_id, start_posn, dim, epsilon = None, gamma = None, alpha = None):

        super().__init__(actor_id, start_posn, PREDATOR, True)

        # q_mat has (2n-1)^2 + 1 rows and 5 columns, since there are (2n-1)^2
        # different states (+1 is for the situation where there is no sheep)
        # and 5 different actions for the actor to take
        self.q_mat = np.matrix(((2*dim-1)**2 + 1)*[5*[0]])
        # initialize epsilon
        if epsilon is None:
            self.epsilon = 0.01
        else:
            self.epsilon = epsilon

        # initialize gamma
        if gamma is None:
            self.gamma = 0.99
        else:
            self.gamma = gamma

        # initialize alpha
        if alpha is None:
            self.alpha = 0.1
        else:
            self.alpha = alpha

        self.actions = [NORTH,SOUTH,EAST,WEST,NA]
        self.dim = dim
        self.prev_state = int(-1)
        self.prev_action = int(-1)

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
            distance = np.subtract(self.posn, closest_sheep)
            state_ind = self._dist_to_state_index(distance)
            return state_ind

    def act(self, observer):
        state = self.get_state(observer)

        # XXX choose one of the following two XXX #
        q = self.q_mat[int(state),:].tolist()[0] # if you want to run fresh
        # q = self.q_mat[int(state),:].tolist() # if you want to read in a saved q matrix

        max_q = max(q)
        if random.random() < self.epsilon:
            probs = [i + (max_q + 0.01)*np.random.rand() for i in q]
            sum_p = sum(probs)
            probs = [float(i)/sum_p for i in probs]
            action_ind = np.random.choice(range(len(q)), p = np.array(probs))
        else:
            maxes = [i for i, x in enumerate(q) if x == max_q]
            action_ind = np.random.choice(maxes)

        action = self.actions[action_ind]
        self.prev_state = int(state)
        self.prev_action = int(action_ind)
        return action

    def give_feedback(self, observer):
        """
        :param observer: the observer class
        :return: nada - just updates the Q matrix
        """
        state = self.get_state(observer)

        if state == self._dist_to_state_index([0,0]):
            r = 1000.0
            self.epsilon *= 0.99
        else:
            r = 0.0


        self.q_mat[self.prev_state,self.prev_action] = \
            (1-self.alpha)*self.q_mat[self.prev_state,self.prev_action] + \
            self.alpha*(r + self.gamma*self.q_mat[state].max())
        # if np.any(self.q_mat[self.prev_state]):
            # print(self.q_mat[self.prev_state])
            # print(self.prev_state)
            # print(state)

    def write_q(self,outfile):
        np.save(outfile, self.q_mat)

    def read_q(self,outfile):
        self.q_mat = np.load(outfile)

    def _dist_to_state_index(self,distance):
        distance = np.add(distance, (self.dim - 1, self.dim - 1))
        return (2*self.dim-1)*distance[0] + distance[1]

if __name__ == '__main__':
    test = np.mat([[1,2,3],[2,3,4]])
    print(test[1].max())
    test[1] = (1-0.1)*test[0] + 0.1*(0.8*(test[1].max()))
    print(test)
