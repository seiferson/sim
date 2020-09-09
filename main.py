#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils as u
import math as m
import pygame as d
import config as c
import random as r
from Entity import Entity


def draw_text(display, str, pos, color, font_renderer):
    label = font_renderer.render(str, 1, color)
    display.blit(label, pos)


def handle_right_mouse_down(pos, status):
    status['dragging'] = True
    status['origin'] = pos


def handle_right_mouse_dragging(pos, status):
    if status['dragging']:
        d = u.calc_distance(status['origin'], pos)
        θ = u.calc_θ(status['origin'], pos)
        p = u.calc_point(θ, d/5, status['viewport'])
        if u.is_point_within_rect(c.MAP_LEN - c.SCR_LEN, c.MAP_WID - c.SCR_WID, p):
            status['viewport'] = p


def handle_right_mouse_up(pos, status):
    status['dragging'] = False
    status['origin'] = None


def handle_left_mouse_down(pos, status):
    pass


d.init()
display = d.display.set_mode((c.SCR_LEN, c.SCR_WID))
clock = d.time.Clock()
font_renderer = d.font.Font('font.ttf', c.FONT_SIZE)
time = 0
status = {
    'dragging': False,
    'origin': None,
    'viewport': (0, 0),
    'entities': [],
    'resources': [],
    'env': []
}

for i in range(0, c.INITIAL_ENTITIES):
    p = u.random_point(15)
    θ = r.randint(0, 360)
    name = u.random_name()
    color = u.random_color()
    gender = '♀'
    entity = Entity(p, name, 60, 3, color, 10, gender, θ)
    status['entities'].append(entity)
"""
origin = u.get_random_point(15)
end = None

while not end:
    end = u.calc_point(r.randint(0, 360), 200, origin)
    if not u.is_point_within_rect(c.MAP_LEN, c.MAP_WID, end):
        end = None

status['env'].append((origin, end))"""


while True:
    display.fill(c.BACKGROUND_COLOR)

    p1 = (c.SCR_LEN-115, 15)
    p2 = (c.SCR_LEN-115, 115)
    p3 = (c.SCR_LEN-15, 115)
    p4 = (c.SCR_LEN-15, 15)

    d.draw.polygon(display, c.COLORS['BLACK'], (p1, p2, p3, p4, p1), 2)

    x = (status['viewport'][u.X] * 100 / c.MAP_LEN) + c.SCR_LEN - 115
    y = (status['viewport'][u.Y] * 100 / c.MAP_WID) + 15

    p5 = (x, y)

    x = ((status['viewport'][u.X] + c.SCR_LEN) * 100 / c.MAP_LEN) + c.SCR_LEN - 115
    y = ((status['viewport'][u.Y] + c.SCR_WID) * 100 / c.MAP_WID) + 15

    p6 = (x, y)
    p7 = (p5[u.X], p6[u.Y])
    p8 = (p6[u.X], p5[u.Y])

    d.draw.polygon(display, c.COLORS['WHITE'], (p5, p7, p6, p8, p5), 1)

    title = 'Time: ' + str(m.floor(time / 24))
    p = (m.floor(c.SCR_LEN / 2), 15)
    draw_text(display, title, p, c.COLORS['BLACK'], font_renderer)

    #p9 = u.get_viewport_pos(status['env'][0][0], status['viewport'])
    #p10 = u.get_viewport_pos(status['env'][0][1], status['viewport'])
    #d.draw.line(display, u.WHITE, p9, p10, 1)

    r.shuffle(status['entities'])
    for entity in status['entities']:
        p = u.calc_viewport_pos(entity.pos, status['viewport'])
        if p:
            d.draw.polygon(display, entity.color, entity.get_polygon(p), 2)
            draw_text(display, str(entity), p, c.COLORS['TEAL'], font_renderer)
            d.draw.polygon(display, entity.color, entity.get_sens_polygon(p), 1)
        entity.do(status)

    for event in d.event.get():
        if event.type == d.QUIT:
            d.quit()
            quit()
        elif event.type == d.MOUSEBUTTONDOWN and event.button == u.RIGHT:
            handle_right_mouse_down(event.pos, status)
        elif event.type == d.MOUSEBUTTONUP and event.button == u.RIGHT:
            handle_right_mouse_up(event.pos, status)
        elif event.type == d.MOUSEBUTTONDOWN and event.button == u.LEFT:
            handle_left_mouse_down(event.pos, status)
        elif event.type == d.MOUSEMOTION:
            handle_right_mouse_dragging(event.pos, status)

    d.display.update()
    clock.tick(c.FPS)
    time += 1
