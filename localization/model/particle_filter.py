import util.event as E
import numpy as np
import bisect
import random
import math

def distance(p,q):
    p_x,p_y = p
    q_x, q_y = q
    return np.sqrt(np.square((p_x-q_x))+np.square((p_y-q_y)))

def get_alpha():

    pass


class WeightedDistribution(object):
    def __init__(self,current_scores):
        '''

        :param state: dict: k time particles dict
        '''
        accum = 0.0
        self.distribution = []
        self.state = []
        for i in range(len(current_scores)):
            if current_scores[i] > 0:
                self.state.append(i)
                accum += current_scores[i]
                self.distribution.append(accum)


    def pick(self):
        try:
            return self.state[bisect.bisect_left(self.distribution, random.uniform(0, 1))]
        except IndexError:
            # Happens when all particles are improbable w=0
            raise

class ParticleFilter:
    def __init__(self,arg,feature_points):
        self.n_particles = arg.n_particles
        self.map_info = arg.map_info
        self.particles = E.Particle()
        self.time_step = 0
        self.events = []
        self.gamma = arg.gamma
        self.D = arg.D
        self.feature_points = feature_points
        self.f = arg.focal_d
        #format of feature points [(1,2),(2,3),...]

        self.init_particle()

    def init_particle(self):
        assert self.time_step == 0, "wrong initial"
        h_max,w_max = self.map_info
        poses = []
        for i in range(self.n_particles):
            x = np.random.rand() * h_max
            y = np.random.rand() * w_max
            r = np.random.rand() * 2*math.pi
            new_particle = E.Pose(x,y,r)
            poses.append(new_particle)
        self.particles.update_Pose(self.time_step,poses)
        scores = self.calculate_score()
        self.particles.update_Score(0, scores)

        self.increment_time() # start the first estimation

    def find_min(self,r,e):
        #F_H(r)
        cur_min = None
        for feature_ in self.feature_points:
            x = distance(feature_,e)
            h = x*self.D/r

            if cur_min is None:
                cur_min = h
            else:
                if h < cur_min:
                    cur_min = h
        return cur_min

    def update_poses(self,delta_r,delta_theta):
        assert self.time_step >= 1,"can not update poses in time=0"
        pre_pose = self.particles.get_k_Particle(self.time_step-1)["poses"]
        Poses = []
        for i in range(self.n_particles):
            M_x = np.random.normal(loc=0, scale=delta_r)
            M_y = np.random.normal(loc=0, scale=delta_r)
            M_r = np.random.normal(loc=0, scale=delta_theta)
            pre_x,pre_y,pre_r = pre_pose[i].state
            x = pre_x + M_x
            y = pre_y + M_y
            r = pre_r + M_r
            new_Pose = E.Pose(x, y, r)
            Poses.append(new_Pose)
        self.particles.update_Pose(self.time_step, Poses)
        return Poses

    def calculate_score(self,pre_scores=None):
        if pre_scores is None:
            pre_scores = np.zeros((self.n_particles))
        new_scores = np.zeros((self.n_particles))
        # min d_{ray}(r,h)
        '''
        we have known all of feature points in this map, and here, we compare the event
        '''
        r = np.zeros((self.n_particles,))
        params = self.events[-1].get_param
        e_x = params['x']
        e_y = params['y']
        current_poses = self.particles.get_k_Particle(self.time_step)["poses"]
        assert len(current_poses) == self.n_particles, "some wrong in _history"
        for i, p in enumerate(current_poses):
            p_x, p_y,_ = p.state
            p_e_d = distance((e_x, e_y), (p_x, p_y))
            Wpx = p_e_d / self.f
            r = np.sqrt((np.square(self.D) + np.square(p_e_d)))
            min_h = self.find_min(r, (e_x, e_y))
            update_number = np.exp(-1 / 2 * np.square(min_h / (self.gamma * Wpx)))
            alpha = 0.5  # need to change!!!!!!!
            new_scores[i] = pre_scores[i] + alpha * update_number
        return new_scores

    def update_scores(self):
        assert self.time_step >= 1, "can not update poses in time=0"
        pre_scores = self.particles.get_k_Particle(self.time_step-1)["scores"]
        new_scores = self.calculate_score(pre_scores=pre_scores)
        self.particles.update_Score(self.time_step, new_scores)




    def increment_time(self):
        self.time_step += 1
        pass

    def get_time_step(self):
        return self.time_step

    def resampling(self):
        new_particles = {"pose":[],"scores":np.zeros(self.n_particles,)}
        current_poses = self.particles.get_k_Particle(self.time_step)["pose"]
        current_scores = self.particles.get_k_Particle(self.time_step)["scores"]
        new_poses = []
        new_scores = np.zeros((self.n_particles,))

        # Normalise weights
        sum = current_scores.sum()
        if sum:
            for i in range(len(current_scores)):
                current_scores[i] = current_scores[i]/sum

        # create a weighted distribution, for fast picking
        dist = WeightedDistribution(current_scores)

        for i in range(len(self.n_particles)):
            index = dist.pick()

            new_poses.append(current_poses[index])
            new_scores[i] = current_scores[index]

        self.particles.update_Pose(self.time_step,new_poses)
        self.particles.update_Score(self.time_step,new_scores)


    def update_event(self,event):
        new_event = event
        self.events.append(new_event)




