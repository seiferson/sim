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


def clear_screen(display):
    display.fill(c.BACKGROUND_COLOR)


def draw_mouse_pos(display):
    m_pos = d.mouse.get_pos()

    p1 = (m_pos[u.X], m_pos[u.Y] + 10)
    p2 = (m_pos[u.X], m_pos[u.Y] - 10)
    
    d.draw.polygon(display, c.COLORS['BLACK'], (p1, p2), 1)
    
    p3 = (m_pos[u.X]+10, m_pos[u.Y])
    p4 = (m_pos[u.X]-10, m_pos[u.Y])
    
    d.draw.polygon(display, c.COLORS['BLACK'], (p3, p4), 1)


def set_title(display, time):
    title = 'Time: ' + str(m.floor(time / c.FPS))
    p = (m.floor(c.SCR_LEN / 2), 15)
    draw_text(display, title, p, c.COLORS['BLACK'], font_renderer)


def draw_minimap(display, status):
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


def handle_keyboard_c(status):
    wp = d.mouse.get_pos()
    x = wp[u.X] + status['viewport'][u.X]
    y = wp[u.Y] + status['viewport'][u.Y]
    p = (x, y)
    θ = r.randint(0, 360)
    name = u.random_name()
    color = c.COLORS['BLACK']
    gender = u.random_gender()
    entity = Entity(p, name, 60, 3, color, 10, gender, θ)
    status['entities'].append(entity)


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

while True:
    clear_screen(display)
    draw_minimap(display, status)
    set_title(display, time)
    draw_mouse_pos(display)

    r.shuffle(status['entities'])
    for entity in status['entities']:
        p = u.calc_viewport_pos(entity.pos, status['viewport'])
        d.draw.polygon(display, entity.color, entity.get_polygon(p), 2)
        draw_text(display, str(entity), (p[u.X], p[u.Y] + 20), entity.color, font_renderer)
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
        elif event.type == d.KEYDOWN and event.key == d.K_c:
            handle_keyboard_c(status)

    d.display.update()
    clock.tick(c.FPS)
    time += 1
