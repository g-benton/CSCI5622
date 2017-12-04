import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Prey(Actor):
    """A simple Prey class."""

    def __init__(self, actor_id, start_posn, dim, epsilon = None):
        self.prev_posn = None
        self.status = "ALIVE"

        super().__init__(actor_id, start_posn, PREY, False)

        self.q_mat = np.matrix(((2*dim-1)**2 + 1)*[5*[0]])
        # initialize epsilon
        if epsilon is None:
            self.epsilon = 0.01
        else:
            self.epsilon = epsilon

        self.actions = [NORTH,SOUTH,EAST,WEST,NA]
        self.dim = dim
        self.prev_state = int(-1)
        self.prev_action = int(-1)
        self.alpha = 0.1
        self.gamma = 0.99

    def get_state(self, observer):
        """
        get location of the closest predator
        """
        closest_predator = observer.get_closest(PREDATOR, self.posn)
        if closest_predator is None:
            return int(-1) # so the state goes to the last row of Q
        else:
            distance = np.subtract(self.posn, closest_predator)
            state_ind = self._dist_to_state_index(distance)
            return state_ind


    def act(self, observer):
        """
        update the position of the prey
        """
        # get state and extract the q matrix values #
        state = self.get_state(observer)
        q = self.q_mat[int(state), :].tolist()[0]

        # can't have negative probs, so scale everything to be nonnegative
        q = [i + min(q) for i in q]

        max_q = max(q)

        if random.random() < self.epsilon:
            # get raw rewards and compute the normalization const. #
            # print(q)
            probs = [i + (max_q + 0.01)*np.random.rand() for i in q]
            sum_probs = sum(probs)

            # normalize to probabilities
            probs = [float(i)/sum_probs for i in probs]

            # make a choice based on q matrix #
            action_ind = np.random.choice(range(len(q)), p = np.array(probs))
        else:
            # what does this do? 
            maxes = [i for i, x in enumerate(q) if x == max_q]
            action_ind = np.random.choice(maxes)

        action = self.actions[action_ind]
        self.prev_state = int(state)
        self.prev_action = int(action_ind)

        return action

        # possible movements
        # options = [NORTH, SOUTH, WEST, EAST]
        # prob_wght = 0.1
        #
        # if(self.prev_posn is None):
        #     # random choice if first move
        #     return random.choice(options)
        # else:
        #     # augment probabilities based on previous posn
        #     tuple_diff = tuple(np.subtract(self.posn, self.prev_posn))
        #     # tuple_diff = (0, 1)
        #     probs = [0.25 + prob_wght*tuple_diff[1],
        #              0.25 - prob_wght*tuple_diff[1],
        #              0.25 - prob_wght*tuple_diff[0],
        #              0.25 + prob_wght*tuple_diff[0]]
        #     # print(probs)
        #     return np.random.choice(options, size=1, p=probs)[0]

    def give_feedback(self, observer):
        """
        observer - the observer class
        no returns
        updates the q matrix for the learner
        """

        state = self.get_state(observer)

        if state == self._dist_to_state_index([0,0]):
            # if the prey and predator are overlapping then HUGE negative reward
            r = -1000
            self.epsilon *=0.99
        else:
            # otherwise give the prey something for continiuing to be alive.
            r = 0.1

        # standard q matrix update algorithm #
        self.q_mat[self.prev_state, self.prev_action] = \
                (1-self.alpha)*self.q_mat[self.prev_state,self.prev_action] + \
                self.alpha*(r + self.gamma*self.q_mat[state].max())

    def _dist_to_state_index(self,distance):
        distance = np.add(distance, (self.dim - 1, self.dim - 1))
        return (2*self.dim-1)*distance[0] + distance[1]


    ## matrix methods ##

    def write_q(self, outfile):
        np.save(outfile, self.q_mat)

    def read_q(self, outfile):
        self.q_mat = np.load(outfile)

    ## XXX this is old stuff I think XXX ##

    def update_posn(self, new_posn):
        """
        takes in tuple of next posn to move to
        updates the vars posn and prev_posn
        returns nothing
        """
        self.prev_posn = self.posn
        self.posn = new_posn

    def die(self):
        self.status = "DEAD"
