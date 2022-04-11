import util.event as E
import numpy as np
import bisect
import random
import math
from util import tools


def distance(p,q):
    p_x,p_y,p_z = p
    q_x, q_y, q_z = q
    return np.sqrt(np.square((p_x-q_x))+np.square((p_y-q_y))+np.square((p_z-q_z)))



class WeightedDistribution(object):
    def __init__(self,current_scores):
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
            print('Happens when all particles are improbable w=0')
            raise

class ParticleFilter:
    def __init__(self,arg,feature_points):
        '''
        n_particles: the number of particles in this Filter
        map_info: the information of map

        '''
        self.n_particles = arg.n_particles
        self.map_info = arg.map_info
        self.particle_list = []
        self.time_step = 0
        self.gamma = arg.gamma
        self.transform = tools.Transform(arg)
        self.D = arg.D
        self.feature_points = feature_points
        self.f = arg.focal
        self.G0 = arg.G0
        self.Wpx = self.cal_Wpx()
        self.theta = 1
        #format of feature points [(1,2),(2,3),...]
        self.alpha = self.cal_alpha()

        self.init_particle()

    def init_particle(self):
        assert self.time_step == 0, "wrong initial"
        init_score = 1  # /self.n_particles
        h_max = w_max = 25
        poses = []
        for i in range(self.n_particles):
            x = random.uniform(-1,1) * h_max
            y = random.uniform(-1,1) * w_max # \pm 25 cm
            r = random.uniform(0,1) * 2 * np.pi

            new_particle = E.Pose(x,y,r)
            temp_particle = E.Particle()
            temp_particle.update_Pose(new_particle)
            temp_particle.update_Score(init_score)
            self.particle_list.append(temp_particle)

    def get_particles(self):
        return self.particle_list


    def update(self,event,pre_particles):
        min_h_list = []
        event_param = event.get_param()
        e_x = event_param['x']
        e_y = event_param['y']
        e_x, e_y, e_z = self.transform.pixel2image(e_x,e_y)
        for i,particle in enumerate(pre_particles):
            pose = particle.get_pose()
            p_x, p_y, p_r = pose.state
            # update pose
            delta_r = self.Wpx / self.G0
            h,w = self.map_info
            S = min(h,w)
            #S = 100
            if self.theta==1:
                delta_theta = 4/(S*self.G0) # 0.0796 degree when G0=8
            elif self.theta==2:
                delta_theta = 0.2 * 2* np.pi/360 # 0.2 degree
            # delta_theta = 0.2 * 2* np.pi/360 # 0.2 degree
            elif self.theta == 3:
                delta_theta = 0.5 * 2 * np.pi / 360  # 0.5 degree
            else:
                delta_theta = 1 * 2* np.pi/360 # 1 degree
            # delta_theta = 0.5 * 2 * np.pi / 360  # 0.5 degree

            #delta_theta = (2/360)*2*np.pi
            M_x = np.random.normal(loc=0, scale=delta_r)
            M_y = np.random.normal(loc=0, scale=delta_r)
            M_r = np.random.normal(loc=0, scale=delta_theta)
            x = p_x + M_x
            y = p_y + M_y
            r = p_r + M_r
            r = tools.valid_angle(r)
            # r = np.pi/2
            new_pose = E.Pose(x,y,r)
            self.particle_list[i].update_Pose(new_pose)
            # update score
            #some new
            new_p_x, new_p_y, new_p_r = new_pose.state
            e_x, e_y, e_z = self.transform.image2ref(e_x, e_y, e_z, new_pose)
            R = distance((e_x, e_y, e_z), (new_p_x, new_p_y, 0))
            min_h = self.find_min(R, (e_x, e_y, e_z))
            min_h_list.append(min_h)
            update_number = np.exp(-1 / 2 * np.square(min_h / (self.gamma * self.Wpx)))
            pre_score = particle.get_score()
            score = pre_score + self.alpha * update_number
            self.particle_list[i].update_Score(score)
        minimum = min(min_h_list)
        return minimum

    def update_with_batch(self,events,pre_particles):
        '''
        update pose and scores
        :param events: a batch of events
        :param pre_particles: particles in last iteration
        :return:
        '''
        if len(events) == 0:
            b = 0
        else:
            b = len(events)
        for i,particle in enumerate(pre_particles):
            # update pose
            pose = particle.get_pose()
            p_x, p_y, p_r = pose.state
            delta_r = self.Wpx / self.G0 # 0.11/8 cm
            h,w = self.map_info
            S = min(h,w)
            #S = 100
            if self.theta == 1:
                delta_theta = 4 / (S * self.G0)  # 0.0796 degree when G0=8
            elif self.theta == 2:
                delta_theta = 0.2 * 2 * np.pi / 360  # 0.2 degree
            # delta_theta = 0.2 * 2* np.pi/360 # 0.2 degree
            else:
                delta_theta = 0.5 * 2 * np.pi / 360  # 0.5 degree
            M_x = np.random.normal(loc=0, scale=delta_r)
            M_y = np.random.normal(loc=0, scale=delta_r)
            M_r = np.random.normal(loc=0, scale=delta_theta)
            x = p_x + M_x
            y = p_y + M_y
            r = p_r + M_r
            r = tools.valid_angle(r)
            # r = np.pi/2
            new_pose = E.Pose(x,y,r)
            self.particle_list[i].update_Pose(new_pose)

            # only update scores when there are events
            if b != 0:
                sum = 0
                for event in events:
                    score_event_param = event.get_param()
                    score_e_x = score_event_param['x']
                    score_e_y = score_event_param['y']
                    score_e_x_i, score_e_y_i, score_e_z_i = self.transform.pixel2image(score_e_x, score_e_y)
                    score_e_x_r, score_e_y_r, score_e_z_r = self.transform.image2ref(score_e_x_i, score_e_y_i, score_e_z_i, new_pose)
                    new_p_x, new_p_y, new_p_r = new_pose.state
                    R = distance((score_e_x_r, score_e_y_r, score_e_z_r), (new_p_x, new_p_y, 0))
                    min_h = self.find_min(R, (score_e_x_r, score_e_y_r, score_e_z_r))
                    update_number = np.exp(-1 / 2 * np.square(min_h / (self.gamma * self.Wpx)))
                    sum += update_number
                pre_score = particle.get_score()
                score = pre_score + self.alpha * sum / b
                self.particle_list[i].update_Score(score)



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
    def find_min_V2(self,r,e):
        #F_H(r)
        cur_min = None
        for feature_ in self.feature_points:
            x = distance(feature_,e)

            if cur_min is None:
                cur_min = x
            else:
                if x < cur_min:
                    cur_min = x
        return cur_min



    def cal_Wpx(self):
        Wpx = 0.002 * self.D / self.f
        #0.11
        return Wpx
    def cal_alpha(self):
        return -math.log(1-0.95)/(self.G0+1)

    def update_G0(self,G0):
        self.G0 = G0


    def increment_time(self):
        self.time_step += 1
        pass

    def get_time_step(self):
        return self.time_step

    def normalize_score(self,scores):
        total = sum(scores)
        if total:
            for i in range(len(scores)):
                scores[i] = scores[i] / total
        return scores

    def resampling(self,noisy=True):
        new_particle_list = []
        current_poses = []
        current_scores = []
        for i,particle in enumerate(self.particle_list):
            current_poses.append(particle.get_pose())
            current_scores.append(particle.get_score())


        # Normalise weights
        current_scores = self.normalize_score(current_scores)


        # get an probibility density distribution
        # accumulative propability
        dist = WeightedDistribution(current_scores)

        for i in range(self.n_particles):
            index = dist.pick()
            if noisy:
                new_pose=current_poses[index].add_noise()
            else:
                new_pose=current_poses[index]
            new_score = current_scores[index]
            new_particle = E.Particle()
            new_particle.update_Pose(new_pose)
            new_particle.update_Score(new_score)
            new_particle_list.append(new_particle)

        self.particle_list = list(new_particle_list)






