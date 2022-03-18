# ------------------------------------------------------------------------
# coding=utf-8
# ------------------------------------------------------------------------
#
#  Created by Martin J. Laubach on 2011-11-15
#
# ------------------------------------------------------------------------

import math
import turtle
import random
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

# from pyecharts.charts import HeatMap

# turtle.tracer(50000, delay=0)
# turtle.register_shape("dot", ((-3,-3), (-3,3), (3,3), (3,-3)))
# turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))
# turtle.speed(0)
# turtle.title("Poor robbie is lost")
#
# UPDATE_EVERY = 0
# DRAW_EVERY = 0

def draw_HeatMap(data,name=None):
    xs = list(range(-25,26))
    ys = list(range(35,-16,-1))

    sns.heatmap(data,cbar=False,xticklabels=False,yticklabels=False)
    #heatmap = fig.get_figure()
    #heatmap.savefig(name)
    plt.show()

def save_HeatMap(data,name=None):
    xs = list(range(-25,26))
    ys = list(range(35,-16,-1))

    fig = sns.heatmap(data,cbar=False,xticklabels=False,yticklabels=False)
    heatmap = fig.get_figure()
    heatmap.savefig(name)


def draw_partiles(particles,max):
    xs = []
    ys = []
    m_x, m_y = max
    for p in particles:
        pose = p.get_pose()
        x,y,r = pose.state
        xs.append(x)
        ys.append(y)
    colors1 = '#00CED1'
    colors2 = '#DC143C'
    area = np.pi * 4 ** 2
    # 画散点图
    plt.scatter(xs, ys, s=area, c=colors1, alpha=0.4, label='particles')
    plt.scatter(m_x, m_y, s=area, c=colors2, alpha=0.4, label='maximum')

    plt.show()

def draw_angle(particles,max_r):
    rs = []
    for p in particles:
        pose = p.get_pose()
        x, y, r = pose.state
        rs.append(r)
    sns.displot(rs,bins=20)
    plt.vlines(max_r, 0, 1, color="red")
    plt.show()

if __name__ == "__main__":
    data = np.random.rand(25,25)
    draw_HeatMap(data)

