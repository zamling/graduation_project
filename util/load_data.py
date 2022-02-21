import numpy as np
import pandas as pd
import os
from util import event as E
data_map = {'single':'single_dot.txt',
            'tone':'tone_dots.txt',
            'triangle':'triangle_dots.txt',
            'shape':'shapes_dots.txt',
            'random':'random_dots.txt',
            'triangle2':'triangle_all.txt'}
root = "C:\git\graduation_project\Data"
feat_map = {
    'triangle': [[-5.8,0,46],[9.4,0,46],[0,6.0,46]],
    'triangle2': [[-5.8,0,46],[9.4,0,46],[0,6.0,46]]
}

def dataLoader(name):
    if name in data_map:
        filename = data_map[name]
    else:
        raise ValueError("wrong data type name {}".format(name))

    path = os.path.join(root,filename)
    results = []
    with open(path,encoding='utf-8',errors='ignore') as f:
        data = f.readlines()
    for event in data:
        event_list = event.strip().split(',')
        event_list = list(map(lambda x:int(x),event_list))
        event = E.Event(x=event_list[1],y=event_list[2],p=event_list[3],t=event_list[0])
        results.append(event)
    return results

class batch_data:
    def __init__(self,B,event_list):
        self.B = B
        self.current_index = 0
        self.event_list = event_list
        self.length = len(event_list)//B
    def __len__(self):
        return self.length

    def __iter__(self):
        return self

    def __next__(self):
        output = []
        for i in range(self.B):
            output.append(self.event_list[self.current_index+i])
        self.current_index += self.B
        return output





def getFeaturePoints(name,expand=True):
    featpoints = []
    if name == 'triangle':
        points = feat_map['triangle']
        for point in points:
            featpoints.append(point)
            if expand is True:
                lt = list(point)
                lt[0] -= 0.5
                lt[1] += 0.5
                featpoints.append(lt)
                lb = list(point)
                lb[0] -= 0.5
                lb[1] -= 0.5
                featpoints.append(lb)
                rt = list(point)
                rt[0] += 0.5
                rt[1] += 0.5
                featpoints.append(rt)
                rb = list(point)
                rb[0] += 0.5
                rb[1] -= 0.5
                featpoints.append(rb)
        return featpoints





    pass



if __name__ == "__main__":
    event_list = dataLoader('shape')




