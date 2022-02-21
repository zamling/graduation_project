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

# turtle.tracer(50000, delay=0)
# turtle.register_shape("dot", ((-3,-3), (-3,3), (3,3), (3,-3)))
# turtle.register_shape("tri", ((-3, -2), (0, 3), (3, -2), (0, 0)))
# turtle.speed(0)
# turtle.title("Poor robbie is lost")
#
# UPDATE_EVERY = 0
# DRAW_EVERY = 0

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

class Maze(object):
    def __init__(self):
        self.width   = 50
        self.height  = 50
        turtle.setworldcoordinates(0, 0, self.width, self.height)
        self.blocks = []
        self.update_cnt = 0
        self.one_px = float(turtle.window_width()) / float(self.width) / 2


    def weight_to_color(self, weight):
        return "#%02x00%02x" % (int(weight * 255), int((1 - weight) * 255))

    def is_in(self, x, y):
        if x < 0 or y < 0 or x > self.width or y > self.height:
            return False
        return True

    def show_mean(self, x, y, confident=False):
        if confident:
            turtle.color("#00AA00")
        else:
            turtle.color("#cccccc")
        turtle.setposition(x, y)
        turtle.shape("circle")
        turtle.stamp()

    def show_particles(self, particles):
        self.update_cnt += 1
        if UPDATE_EVERY > 0 and self.update_cnt % UPDATE_EVERY != 1:
            return

        turtle.clearstamps()
        turtle.shape('tri')

        draw_cnt = 0
        px = {}
        for p in particles:
            draw_cnt += 1
            if DRAW_EVERY == 0 or draw_cnt % DRAW_EVERY == 1:
                # Keep track of which positions already have something
                # drawn to speed up display rendering
                pose = p.get_pose()
                score = p.get_score()
                x,y,r = pose.state
                r = r*360/(2*math.pi)
                xy = [x,y]
                scaled_x = int(x * self.one_px)
                scaled_y = int(y * self.one_px)
                scaled_xy = scaled_x * 10000 + scaled_y
                if not scaled_xy in px:
                    px[scaled_xy] = 1
                    turtle.setposition(*xy)
                    turtle.setheading(r)
                    turtle.color(self.weight_to_color(score))
                    turtle.stamp()

    def show_robot(self, robot):
        turtle.color("green")
        turtle.shape('turtle')
        turtle.setposition(*robot.xy)
        turtle.setheading(90 - robot.h)
        turtle.stamp()
        turtle.update()




