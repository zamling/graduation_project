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
# root = "C:\git\graduation_project\Data"

# root = "/data1/zem/graduate_project/Data"

feat_map = {
    'triangle': [[-5.8,0,46],[9.4,0,46],[0,6.0,46]],
}

def dataLoader(args, name):
    if name in data_map:
        filename = data_map[name]
    else:
        raise ValueError("wrong data type name {}".format(name))
    root = args.data_root

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
    def __init__(self,event_list,is_positive=False):
        self.current_index = 0
        self.event_list = event_list
        self.is_positive = is_positive

    def get_data(self,B):
        output = []
        for i in range(B):
            if self.is_positive:
                temp_event = self.event_list[self.current_index+i]
                pol = temp_event.get_param()['p']
                if pol == 1:
                    output.append(self.event_list[self.current_index + i])
            else:
                output.append(self.event_list[self.current_index+i])
        self.current_index += B
        return output

class TimeDataIter:
    def __init__(self,event_list,interval,is_positive=False):
        self.event_list = event_list
        self.interval = interval
        self.iter = batch_data(event_list,is_positive)
        self.time = 0
        self.current = 0
        self.terminal = len(event_list)
    def iter_data(self):
        event_time = self.event_list[self.current].get_param()['t']
        count = 0
        while event_time < self.time + self.interval:
            count += 1
            self.current += 1
            if self.current == self.terminal:
                break
            event_time = self.event_list[self.current].get_param()['t']
        self.time += self.interval
        if count == 0:
            return []
        else:
            data = self.iter.get_data(count)
            return data
    def not_end(self):
        return self.current < self.terminal
    def currentEvent(self):
        return self.current







def getFeaturePoints(name,expand=True):
    featpoints = []
    if name == 'triangle':
        points = feat_map['triangle']
        for point in points:
            featpoints.append(point)
            if expand is True:
                # top = list(point)
                # top[1] += 1
                # top[0] += 1
                # featpoints.append(top)
                # bot = list(point)
                # bot[0] -= 1
                # bot[1] -= 1
                # featpoints.append(bot)
                # r = list(point)
                # r[0] += 1
                # r[1] -= 1
                # featpoints.append(r)
                # l = list(point)
                # l[0] -= 1
                # l[1] += 1
                # featpoints.append(l)
                top = list(point)
                top[1] += 1
                featpoints.append(top)
                bot = list(point)
                bot[1] -= 1
                featpoints.append(bot)
                r = list(point)
                r[0] += 1
                featpoints.append(r)
                l = list(point)
                l[0] -= 1
                featpoints.append(l)
                lt = list(point)
                lt[0] -= 0.707
                lt[1] += 0.707
                featpoints.append(lt)
                rt = list(point)
                rt[0] += 0.707
                rt[1] += 0.707
                featpoints.append(rt)
                lb = list(point)
                lb[0] -= 0.707
                lb[1] -= 0.707
                featpoints.append(lb)
                rb = list(point)
                rb[0] += 0.707
                rb[1] -= 0.707
                featpoints.append(rb)
        print('the number of feature point is: {}'.format(len(featpoints)))
        return featpoints




if __name__ == "__main__":
    feature = getFeaturePoints('triangle')
    print(feature)




