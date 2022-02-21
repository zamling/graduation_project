import random
import math
import numpy as np


def valid_angle(angle):
    '''
    limit the angle in [0,2*pi]
    :param angle:
    :return:
    '''
    if angle > 2 * np.pi:
        factor = angle // (2 * np.pi)
        angle = angle - factor * 2 * np.pi

    elif angle < 0:
        temp_angle = -angle
        factor = temp_angle // (2 * np.pi)
        angle = angle + (factor+1) * 2 * np.pi
    return angle


class Transform:
    def __init__(self, arg):
        self.arg = arg
        self.alpha = 0.002


    def pixel2image(self,x,y):
        z_ = self.arg.D
        h,w = self.arg.map_info

        x_ = ((self.arg.D / self.arg.focal) * x - w / 2) * self.alpha
        y_ = ((self.arg.D / self.arg.focal) * y - h / 2) * self.alpha

        return x_ , y_, z_

    def get_rotate_mat(self,theta):
        return np.array([[math.cos(theta), -math.sin(theta),0], [math.sin(theta), math.cos(theta),0],[0,0,1]])


    def image2ref(self,x,y,z,pose):
        px,py,pr = pose.state
        rot_mat = self.get_rotate_mat(pr)
        pos = np.array([x-px,y-py,z])
        ref_pos = np.dot(rot_mat.T,pos)

        return ref_pos[0],ref_pos[1],ref_pos[2]








