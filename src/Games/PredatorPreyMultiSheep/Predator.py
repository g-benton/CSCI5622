import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor

class Predator(Actor):
    """Simple Predator class. """

    def __init__(self, actor_id, start_posn, theta_divides, r_divides, wall_divides):

        # theta_divides is a list of lists. The predator can determine that the K^th closest sheep is
        # in between any of the angles in list K, but it has no more precision than that.

        # r_divides is the same as theta_divides, but for distances (I used the 2-norm). In addition, the predator
        # cannot see beyond the distance that is the last element of r_divides.

        # wall_divides is the same as r_divides, but with the closest wall. Therefore, the information that the predator
        # gets is (direction, distance_index) for the n closest walls, where n is the length of wall_divides

        # in total, the predator will get a list of tuples, (direction, distance), for each sheep and the closest wall.
        # This will be the input into the state space, so the size of the Q-matrix is:
        #
        #  ((# of directions)*(# of distances) + 1)^(# of sheep + 1).
        #
        # The +1 in the exponent comes from finding the location of the wall. The other +1 comes from if the predator
        # can't see the sheep/wall. This can get pretty big as we put in more sheep.

        super().__init__(actor_id, start_posn, PREDATOR, True)

        self.theta_divides = theta_divides
        self.r_divides = r_divides
        self.wall_divides = wall_divides
        self.basis_mat = _make_basis_matrix()
        self.q_mat = np.array(states*[5*[0]])

        self.actions = [NORTH,SOUTH,EAST,WEST,NA]
        self.prev_state = int(-1)
        self.prev_action = int(-1)
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 0.01
        self.decay_per_epoch = 0.01
        self.reward = 1000.0
        self.moves = 0

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
        # get current state of the observer
        state = self.get_state(observer)

        # update the number of moves that the predetor has used
        self.moves += 1

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
            r = self.reward
            self.epsilon *= (1-self.decay_per_epoch)
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

    def _dist_to_state_index(self,sheep_distances,wall_distance):
        # distance is a list of tuples of (x_distance, y_distance)
        # this function returns an an index to the Q-matrix from that

        # first get the direction and distance to the closest wall
        wall = _distance_to_heading(wall_distance)

        sheep = (np.arctan2(wall_distance[0],wall_distance[1]),np.linalg.norm(wall_distance))
        sheep = sorted(sheep, key = lambda x: (x[1], x[2]))

        # extract the "a" matrix, which is the coefficients of a number in base (self.basis_mat)

        a = []

        # do this for each sheep/wall that the wolf sees
        for thetas,rs,dist in zip(self.theta_divides,self.r_divides,distances):
            # if the wolf can't see the wall/
            if np.linalg.norm(dist) > rs[-1]:
                a.append(0)
                continue
            #theta = np.
            #r_ind =

        return np.dot(a,self.basis_mat)

    def _distance_to_heading(self,distance):
        return (np.arctan2(distance[0],distance[1]),np.linalg.norm(distance))

    def _make_basis_matrix(self):
        states_mat = np.array([len(theta) * len(r) + 1 for theta, r in zip(self.theta_divides,self.r_divides)])
        states_mat = np.insert(states_mat,0,len(self.wall_divides) + 1)
        basis = np.cumprod(states_mat)
        return np.insert(np.delete(basis, -1),0,1)

if __name__ == '__main__':
    test0 = (1,2)
    test = np.array([[5,8,10],[2,3,4]])
    print(np.insert(np.delete(test, -1),0,1))
    print(test0)
