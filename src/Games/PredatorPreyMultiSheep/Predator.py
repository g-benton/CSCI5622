import random
import numpy as np
import sys

sys.path.append('../../Grid')
from GridConstants import *
from Actor import Actor


def _make_basis_matrix(wolf_r_divides,wolf_theta_divides,
                       sheep_r_divides, sheep_theta_divides,
                       obs_r_divides,obs_theta_divides,
                       wall_r_divides):

    # make an array with all of the possible states for each actor and wall
    wolf_states_mat = [len(theta) * len(r) + 1 for theta, r in zip(wolf_theta_divides, wolf_r_divides)]
    sheep_states_mat = [len(theta) * len(r) + 1 for theta, r in zip(sheep_theta_divides, sheep_r_divides)]
    obs_states_mat = [len(theta) * len(r) + 1 for theta, r in zip(obs_theta_divides, obs_r_divides)]
    wall_states_mat = [4*len(r) + 1 for r in wall_r_divides]

    states_mat = wolf_states_mat + sheep_states_mat + obs_states_mat + wall_states_mat
    # make an array that acts as a basis to hash states to a state index
    basis = np.cumprod(states_mat)
    num_states = int(basis[-1])
    basis = np.insert(np.delete(basis, -1), 0, 1)
    return (num_states, basis)

class Predator(Actor):
    """Simple Predator class. """

    def __init__(self, actor_id, start_posn,
                 wolf_r_divides, wolf_theta_divides,
                 sheep_r_divides, sheep_theta_divides,
                 obs_r_divides,obs_theta_divides,
                 wall_r_divides, penalty_fraction=0.01,
                 alpha=0.01, gamma=0.8, epsilon=0.25,
                 epsilon_decay_per_epoch=0.01):
        """
        theta_divides is a list of lists. The predator can determine that the K^th closest sheep is
        in between any of the angles in list K, but it has no more precision than that.

        r_divides is the same as theta_divides, but for distances (I used the 2-norm). In addition, the predator
        cannot see beyond the distance that is the last element of r_divides.

        wall_r_divides is the same as r_divides, but with the closest wall. Therefore, the information that the
        predator gets is (direction, distance_index) for the n closest walls, where n is the length of wall_divides

        in total, the predator will get a list of tuples, (direction, distance), for each sheep and the closest wall.
        This will be the input into the state space, so the size of the Q-matrix is:

         ((# of directions)*(# of distances) + 1)^(# of actors + # of walls).

        The +1 in the exponent comes from finding the location of the wall. The other +1 comes from if the predator
        can't see the sheep/wall. This can get pretty big as we put in more actors.

        The penalty fraction is the fraction of the reward that is used for
        penalty if the predator is not catching anything currently.
        """

        super().__init__(actor_id, start_posn, PREDATOR, True)

        self.actions = [NORTH, SOUTH, EAST, WEST, NA]

        self.wolf_theta_divides = wolf_theta_divides
        self.wolf_r_divides = wolf_r_divides
        self.num_wolves_seen = len(wolf_r_divides)

        self.sheep_theta_divides = sheep_theta_divides
        self.sheep_r_divides = sheep_r_divides
        self.num_sheep_seen = len(sheep_r_divides)

        self.obs_theta_divides = obs_theta_divides
        self.obs_r_divides = obs_r_divides
        self.num_obs_seen = len(obs_r_divides)

        self.wall_r_divides = wall_r_divides
        self.num_walls_seen = len(wall_r_divides)

        (self.states,self.basis_mat) = _make_basis_matrix(self.wolf_r_divides,self.wolf_theta_divides,
                                                          self.sheep_r_divides, self.sheep_theta_divides,
                                                          self.obs_r_divides, self.obs_theta_divides,
                                                          self.wall_r_divides)

        self.q_mat = np.array(self.states*[len(self.actions)*[0.0]])
        self.prev_state = int(-1)
        self.prev_action = int(-1)
        self.alpha = alpha # learning rate (consider how random the process is)
        self.gamma = gamma # percent propogated back in Q-matrix equation (consider size of state space)
        self.epsilon = epsilon # percentage of time spent exploring
        self.epsilon_decay_per_epoch = epsilon_decay_per_epoch# decay of epsilon each time the sheep is killed
        self.reward = 10000.0 # reward function (arbitrary)
        if (penalty_fraction is not None and penalty_fraction > 0
            and penalty_fraction < 1):
            self.penalty = -1 * self.reward * penalty_fraction
        else:
            self.penalty = 0
        self.moves = 0 # moves taken by the predator

    def get_state(self,observer):
        """
        :param observer: the observer class
        :return: the index in the Q matrix that corresponds to the state of the predator. Note that the index for the
         q-matrix is the distance vector from base (2*dim - 1) to base 10
        """

        closest_preds = observer.get_k_closest(PREDATOR, self.posn, self.num_wolves_seen + 1)
        closest_preds = [np.subtract(pred,self.posn) for pred in closest_preds]
        closest_preds = closest_preds[1:]

        closest_prey = observer.get_k_closest(PREY, self.posn, self.num_sheep_seen)
        closest_prey = [np.subtract(prey,self.posn) for prey in closest_prey]

        closest_obs = observer.get_k_closest(PREY, self.posn, self.num_obs_seen)
        closest_obs = [np.subtract(obs, self.posn) for obs in closest_obs]

        dim = observer.grid.grid_dim
        walls = [0,1,2,3] # North, South, East, and West, respectively.
        dist_to_walls = [self.posn[1], dim[1] - self.posn[1] - 1, dim[0] - self.posn[0] - 1, self.posn[0]]
        # get the indices of the k closest walls
        closest_walls_inds = np.argpartition(dist_to_walls, self.num_walls_seen)[self.num_walls_seen:]
        closest_walls = [(dist_to_walls[ind],walls[ind]) for ind in closest_walls_inds]

        state_ind = self._dists_to_state_index(closest_preds,closest_prey,closest_obs,closest_walls)

        return state_ind

    def act(self, observer):
        # get current state of the observer
        state = self.get_state(observer)

        # update the number of moves that the predator has used
        self.moves += 1

        # XXX choose one of the following two XXX #
        # q = self.q_mat[int(state),:].tolist()[0] # if you want to run fresh
        q = self.q_mat[int(state),:].tolist() # if you want to read in a saved q matrix

        max_q = max(q)
        if random.random() < self.epsilon:
            probs = [ii + (max_q + 0.01)*np.random.rand() for ii in q]
            min_prob = abs(min(probs))
            probs = [prob + min_prob for prob in probs]
            probs = [float(prob)/sum(probs) for prob in probs]
            action_ind = np.random.choice(range(len(q)), p = np.array(probs))
        else:
            maxes = [ii for ii, x in enumerate(q) if x == max_q]
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

        # Get the amount of prey captured by all predators.
        num_captured = len(observer.get_overlapped_posns())
        if num_captured > 0:
            r = self.reward * num_captured
            self.epsilon *= (1.0-self.epsilon_decay_per_epoch)
        else:
            r = self.penalty

        self.q_mat[self.prev_state,self.prev_action] = \
            float(1.0-self.alpha)*float(self.q_mat[self.prev_state,self.prev_action]) + \
            float(self.alpha)*float(r + self.gamma*self.q_mat[state].max())

    def write_q(self,outfile):
        np.save(outfile, self.q_mat)

    def read_q(self,outfile):
        self.q_mat = np.load(outfile)

    def _dists_to_state_index(self,wolf_distances,sheep_distances,obs_distances,wall_headings):
        # distances is a list of tuples of (x_distance, y_distance)
        # wall_headings is a list of tuples of (wall, distance)
        # this function returns an an index to the Q-matrix from that

        wolf_coefs = self._distance_to_coefs(self.wolf_r_divides, self.wolf_theta_divides, wolf_distances)
        sheep_coefs = self._distance_to_coefs(self.sheep_r_divides, self.sheep_theta_divides, sheep_distances)
        obs_coefs = self._distance_to_coefs(self.obs_r_divides, self.obs_theta_divides, obs_distances)
        wall_coefs = self._wall_distance_to_coefs(wall_headings)

        # extract the "a" matrix, which is the coefficients of a number in base (self.basis_mat)
        a = np.array(wolf_coefs + sheep_coefs + obs_coefs + wall_coefs)
        return np.dot(a,self.basis_mat)

    def _distance_to_coefs(self,r_divides_list,theta_divides_list,distances):

        coefs = []

        num_actors = len(distances)
        num_actors_not_seen = len(theta_divides_list) - num_actors
        theta_divides_list = theta_divides_list[:num_actors]
        r_divides_list = r_divides_list[:num_actors]

        for dist,r_divides,theta_divides in zip(distances,r_divides_list,theta_divides_list):
            theta = np.arctan2(-dist[1],dist[0]) * 180 / np.pi
            r = np.linalg.norm(dist)
            r_ind = next((ii for (ii,r_divide) in enumerate(r_divides) if r <= r_divide), -1)
            if r_ind == -1:
                coefs.append(0)
                continue
            theta_ind = next((ii for (ii,theta_divide) in enumerate(theta_divides) if theta <= theta_divide), 0)
            coefs.append(r_ind*(len(theta_divides)) + theta_ind + 1)

        for ii in range(num_actors_not_seen):
            coefs.append(0)

        return coefs

    def _wall_distance_to_coefs(self,distances):

        coefs = []
        for dist,r_divides in zip(distances,self.wall_r_divides):
            r = dist[0]
            wall = dist[1]
            r_ind = next((ii for (ii, r_divide) in enumerate(r_divides) if r <= r_divide), -1)
            if r_ind == -1:
                coefs.append(0)
            else:
                coefs.append(r_ind*4 + wall + 1)

        return coefs

if __name__ == '__main__':

    sheep_r = 100
    r_divides = [1,2,5,10,20]
    test = next((ii for (ii, r_divide) in enumerate(r_divides) if sheep_r <= r_divide), -1)
