from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('TkAgg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import colorsys
import math


from math import *
def phi(x):
    #'Cumulative distribution function for the standard normal distribution'
    return (1.0 + erf(x / sqrt(2.0))) / 2.0

def open_file():
    with open("dane.dem") as file:
        w, h, x = file.readline().split()
        data = []
        for line in file.readlines():
            data.append(line.split())
    return w, h, x, data

def rozszerz(w, h, data):
    data2 = []
    for i in range(w):
        pom = []
        for j in range(h-1):
            pom.append(data[i][j])
            pom.append((data[i][j]+data[i][j+1])/2)
        pom.append(data[i][h-1])
        data2.append(pom)

    data3 = []
    for i in range(w-1):
        pom = []
        for j in range(2*h-1):
            pom.append((data2[i][j] + data2[i+1][j])/2)
        data3.append(data2[i])
        data3.append(pom)
    data3.append(data2[w-1])
    return data3

def rysuj(w, h, x, data):
    rc('legend', fontsize=10)

    column_width_pt = 800
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, ax = plt.subplots(nrows=1, sharex=True, figsize=(size, size))


    # Create image with two lines and draw gradient on it
    max_wys, min_wys = maxi_mini(data)
    img = np.zeros((w, h, 3))
    sun = [250, 150, 1200]

    katy = []
    for i in range(w):
        pom = []
        for j in range(h):
            if i < w-1 and j < h-1:
                a = [0, 1, data[i+1][j]- data[i][j]]
                b = [1, 0, data[i][j+1] - data[i][j]]
                c = np.cross(a, b)
                kat = angle(c, sun)
                kat = math.degrees(kat)
                kat = kat-90
                pom.append(kat)
        katy.append(pom)

    najwiekszy_kat, najmniejszy_kat  = maxi_mini(katy)
    print(najwiekszy_kat)
    print(najmniejszy_kat)

    for i in range(w):
        for j in range(h):
            img[i, j] = gradient(data[i][j]/max_wys)
            if i < w-1 and j < h-1:
                img[i, j] = gradient3(data[i][j]/max_wys, katy[i][j]/90.0)

    im = ax.imshow(img, aspect='auto')
    im.set_extent([0, 500, 0, 500])
    ax.tick_params(direction = 'in')
    xticks = ax.yaxis.get_major_ticks()
    xticks[0].label1.set_visible(False)
    fig.savefig('my-map.pdf')

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def maxi_mini(data):
    maxi = data[0][0]
    mini = data[0][0]
    for row in data:
        for elem in row:
            if elem > maxi:
                maxi = elem
            if elem < mini:
                mini = elem
    return maxi, mini

def gradient(v):
    return hsv2rgb(2/5 - v*2/5, 1, 1)

def gradient3(v, kat):
    #if kat >= 0.05: # to dla macierzy 500x 500
    #    return hsl2rgb(0.45 - v*0.45, kat*0.2+0.4, 1)
    #return hsl2rgb(0.45 - v*0.45, 0.9-kat, 1)

    if kat >= 0.15:
        return hsl2rgb(0.45 - v*0.45, kat*0.12 + 0.4, 1)
    return hsl2rgb(0.45 - v*0.45, 0.9-kat, 1) #dla data3



def hsl2rgb(h, l, s):
    return  colorsys.hls_to_rgb(h, l, s)


def hsv2rgb(h, s, v):
    return  colorsys.hsv_to_rgb(h, s, v)

w, h, x, data = open_file()
w = int(w)
h = int(h)
data = np.array(data)
data = data.astype(np.float)
data3 = rozszerz(w, h, data)

rysuj(len(data3), len(data3[0]), x, data3)