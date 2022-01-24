import numpy as np
import random
import pandas as pd
from util import tools
class Event:
    '''
    intput data will be converted to this format
    '''
    def __init__(self,x,y,p,t):
        self.x = x
        self.y = y
        self.pol = p
        self.time = t

    def get_param(self):
        return {'x':self.x,
                'y':self.y,
                'p':self.pol,
                't':self.time}
    def __repr__(self):
        return "the event location is: ( {} , {}) \n the polarity is: {}\n the time step is {}".format(self.x,self.y,self.pol,self.time)


def add_noise(level, *coords):
    return [x + random.uniform(-level, level) for x in coords]

def add_little_noise(*coords):
    return add_noise(0.02, *coords)

def add_some_noise(*coords):
    return add_noise(0.1, *coords)

class Particle:
    '''
    the particles log
    '''
    def __init__(self):
        self.score = 0
        self.pose = Pose(0,0,0)

    def update_Pose(self,p=None):
        '''

        :param p: a value of Pose class
        :return: None
        '''
        if p is not None:
            self.pose = p
        else:
            print('ERROR in update Pose')

    def update_Score(self,s=None):
        if s is not None:
            self.score = s
        else:
            print('ERROR in update score')
    def get_pose(self):
        return self.pose
    def get_score(self):
        return self.score


class Pose:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r

    @property
    def state(self):
        return self.x, self.y, self.r

    def add_noise(self,level=1):
        x = self.x+ random.uniform(-level, level)
        y = self.x+ random.uniform(-level, level) # guassion  1 cm 1-2 degree (0, 2pi)
        r = self.x+ random.uniform(-level, level)*2
        r = tools.valid_angle(r)

        return Pose(x,y,r)






#
# if __name__ == "__main__":
#
#     pass







