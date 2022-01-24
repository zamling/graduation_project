import numpy as np
import pandas as pd
import os
import event as E
data_map = {'single':'single_dot.txt',
            'tone':'tone_dots.txt',
            'triangle':'triangle_dots.txt',
            'shape':'shapes_dots.txt',
            'random':'random_dots.txt'}
root = "C:\git\graduation_project\Data"

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

def getFeaturePoints(name):

    pass



if __name__ == "__main__":
    event_list = dataLoader('shape')




