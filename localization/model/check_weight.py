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



class WeightChecker:
    def __init__(self,arg,feature_points):
        '''
        n_particles: the number of particles in this Filter
        map_info: the information of map

        '''
        self.n_particles = arg.n_particles
        self.map_info = arg.map_info
        self.weightMap = np.full((51,51),1/(51*51))
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


    def fix_angle_update(self,events):
        '''
        update scores by events

        :param events: events in current batch
        :return:
        '''
        if len(events)==0:
            b = 0
            return None
        else:
            b = len(events)
        for i in range(self.weightMap.shape[0]):
            for j in range(self.weightMap.shape[1]):
                #generate the current pose
                y_shift = 0
                p_x = j - 25
                p_y = 25 - i + y_shift
                # p_r = np.pi/2
                p_r = 90 * 2 * np.pi / 360 # 90 degree
                new_pose = E.Pose(p_x,p_y,p_r)
                sum = 0
                # update scores
                for event in events:
                    score_event_param = event.get_param()
                    score_e_x = score_event_param['x']
                    score_e_y = score_event_param['y']
                    # transform coordinates
                    score_e_x_i, score_e_y_i, score_e_z_i = self.transform.pixel2image(score_e_x, score_e_y)
                    score_e_x_r, score_e_y_r, score_e_z_r = self.transform.image2ref(score_e_x_i, score_e_y_i, score_e_z_i, new_pose)
                    new_p_x, new_p_y, new_p_r = new_pose.state
                    # calculate the length of ray
                    R = distance((score_e_x_r, score_e_y_r, score_e_z_r), (new_p_x, new_p_y, 0))
                    # find minimum h
                    min_h = self.find_min(R, (score_e_x_r, score_e_y_r, score_e_z_r))
                    # eq. 28 in my report
                    update_number = np.exp(-1 / 2 * np.square(min_h / (self.gamma * self.Wpx)))
                    sum += update_number
                pre_score = self.weightMap[i][j]
                # normalized by batch size b
                score = pre_score + self.alpha * sum / b
                self.weightMap[i][j] = score

    def check_costMatrix(self,events):
        '''
        check the scores map and minimum h
        :param events: events in current batch
        :return: minimum h, score maps
        '''
        print(f'alpha: {self.alpha}')
        if len(events) == 0:
            b = 0
            return 0,0,0
        else:
            b = len(events)
        w,h = self.weightMap.shape
        min_h_map = np.zeros((b,w,h))
        each_update_map = np.zeros((b,w,h))
        update_map = np.zeros_like(self.weightMap)
        for i in range(self.weightMap.shape[0]):
            for j in range(self.weightMap.shape[1]):
                y_shift = 30
                p_x = j - 25
                p_y = 25 - i + y_shift
                p_r = np.pi/2
                new_pose = E.Pose(p_x,p_y,p_r)
                sum = 0
                for k,event in enumerate(events):
                    score_event_param = event.get_param()
                    score_e_x = score_event_param['x']
                    score_e_y = score_event_param['y']
                    score_e_x_i, score_e_y_i, score_e_z_i = self.transform.pixel2image(score_e_x, score_e_y)
                    score_e_x_r, score_e_y_r, score_e_z_r = self.transform.image2ref(score_e_x_i, score_e_y_i, score_e_z_i, new_pose)
                    new_p_x, new_p_y, new_p_r = new_pose.state
                    R = distance((score_e_x_r, score_e_y_r, score_e_z_r), (new_p_x, new_p_y, 0))
                    min_h = self.find_min(R, (score_e_x_r, score_e_y_r, score_e_z_r))
                    min_h_map[k,i,j] = min_h
                    update_number = np.exp(-1 / 2 * np.square(min_h / (self.gamma * self.Wpx)))
                    each_update_map[k,i,j] = self.alpha * update_number
                    sum += update_number
                update_map[i,j] = self.alpha * sum/b

        return min_h_map,each_update_map,update_map


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

    def normalize_weight(self):
        total = sum(self.weightMap)
        self.weightMap = self.weightMap / total

    @property
    def CurrentWeight(self):
        return self.weightMap





