#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random as rn
import config as cn
import math as mt

X = 0
Y = 1

LEFT = 1
RIGHT = 3


def random_point(margin = 0):
    x = rn.randint(margin, cn.MAP_LEN - margin)
    y = rn.randint(margin, cn.MAP_WID - margin)

    return (x, y)


def random_name():
    greek_alphabet = 'αβγΔεΖηθικλμνΞοπρΣτυΦΧΨΩ'

    name = greek_alphabet[rn.randint(0, len(greek_alphabet) - 1)]
    name += greek_alphabet[rn.randint(0, len(greek_alphabet) - 1)]
    name += str(rn.randint(0, 1000))

    return name


def random_color():
    key = list(cn.COLORS)[rn.randint(0, len(cn.COLORS) - 1)]

    while cn.COLORS[key] == cn.BACKGROUND_COLOR:
        key = list(cn.COLORS)[rn.randint(0, len(cn.COLORS) - 1)]

    return cn.COLORS[key]


def calc_viewport_pos(p, v):
    x = p[X] - v[X]
    y = p[Y] - v[Y]

    return (x, y)


def calc_point(θ, d, origin):
    x = mt.floor(mt.cos(mt.radians(θ)) * d) + origin[X]
    y = mt.floor(mt.sin(mt.radians(θ)) * d) + origin[Y]

    return (x, y)


def calc_θ(a, b):
    Δx = b[X] - a[X]
    Δy = b[Y] - a[Y]

    return mt.floor(mt.degrees(mt.atan2(Δy, Δx)))


def calc_distance(a, b):
    Δx = b[X] - a[X]
    Δy = b[Y] - a[Y]

    return mt.sqrt(mt.pow(Δx, 2) + mt.pow(Δy, 2))


def is_point_within_rect(l, w, p):
    return p[X] >= 0 and p[X] <= l and p[Y] >= 0 and p[Y] <= w


def is_point_in_line(s, e, p):
    return False
