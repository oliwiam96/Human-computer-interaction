#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('TkAgg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import colorsys
import math

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True)
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        print(img[0][0])
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)
    fig.savefig('my-gradients.pdf')


def hsv2rgb(h, s, v):
    #return  colorsys.hsv_to_rgb(h, s, v)
    return  hsv2rgb_moj(h, s, v)

def hsv2rgb_moj(h, s, v):
    i = int(h*6.)
    f = (h*6.) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0 -   f))
    i = i%6
    if i == 0:
        return (v, t, p)
    if i == 1:
        return (q, v, p)
    if i == 2:
        return (p, v, t)
    if i == 3:
        return (p, q, v)
    if i == 4:
        return (t, p, v)
    if i == 5:
        return (v, p, q)

    #c = v*s#*math.sin(h*2*math.pi)
    #x = c * (1 - abs( (h*60)%2-1 ))*math.sin(h*2* math.pi)
    #m = v-c
    #if h*360 < 60:
    #    return plus_m(c, x, 0, m)
    #if h*360 < 120:
    #    return plus_m(x, c, 0, m)
    #if h*360 < 180:
    #    return plus_m(0, c, x, m)
    #if h*360 < 240:
    #    return plus_m(0, x, c, m)
    #if h*360 < 300:
    #    return plus_m(x, 0 ,c, m)
    #else:
    #    return plus_m(c, 0, x, m)

def plus_m(r, g, b, m):
    return (r+m, g+m, b+m)

def gradient_rgb_bw(v):
    return (v, v, v)



def gradient_rgb_gbr(v):
    if v < 0.5:
        return (0, 1-v*2, v*2)
    else:
        return (v*2-1, 0, 2-v*2)


def gradient_rgb_gbr_full(v):
    if v < 0.25:
        return (0, 1, v*4)
    if v < 0.5:
        return (0, 1 - (v-0.25)*4, 1)
    if v < 0.75:
        return  ((v-0.5)*4, 0, 1)
    else:
        return (1, 0, 1 - (v-0.75)*4)


def gradient_rgb_wb_custom(v):
    if v < 1/7:
        return (1, 1- v*7, 1)
    if v < 2/7:
        return (1- (v-1/7)*7, 0, 1)
    if v < 3/7:
        return (0, (v-2/7)*7, 1)
    if v < 4/7:
        return (0, 1, 1- (v- 3/7)*7)
    if v < 5/7:
        return ((v- 4/7)*7, 1, 0)
    if v < 6/7:
        return (1, 1- (v-5/7)*7, 0)
    else:
        return (1- (v-6/7)*7, 0, 0)


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    return hsv2rgb((v*2/3)+1/3, 1, 1)

def gradient_hsv_unknown(v):
    return hsv2rgb(1/3 - v*1/3, 0.5, 1)


def gradient_hsv_custom(v):
    return hsv2rgb(v, 1-v, 1)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
