import numpy as np
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
        return "the event location is: ("+self.x+" , "+self.y+") \n the polarity is: "+self.pol+"\n the time step is"+self.time


class Particle:
    '''
    the particles log
    '''
    def __init__(self):
        self._history = {}

    def update_Pose(self,k,p=None):
        poses = []
        if p is not None:
            poses = p
        if k not in self._history:
            self._history[k]={}
        self._history[k]["pose"]=poses

    def update_Score(self, k, s=None):
        poses = []
        scores = []
        if s is not None:
            scores = s
        if k not in self._history:
            self._history[k]={}
        self._history[k]["scores"] = scores

    def get_k_Particle(self,k):
        assert k in self._history, "wrong time steps"
        return self._history[k]

class Pose:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    @property
    def state(self):
        return self.x, self.y

if __name__ == "__main__":
    p = Pose(1,2)
    print(p.state)





