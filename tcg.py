#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils as u
import math as m
import pygame as d
import config as c
import card as tc
import random as r

def draw_text(display, str, pos, color, font_renderer):
    label = font_renderer.render(str, 1, color)
    display.blit(label, pos)

def draw_card(display, font_renderer, card):
    p1 = (30, 30)
    p2 = (30, 300)
    p3 = (220, 300)
    p4 = (220, 30)
    d.draw.polygon(display, c.COLORS['BLACK'], (p1, p2, p3, p4, p1), 1)
    draw_text(display, card.name, (40, 40), c.COLORS['BLACK'], font_renderer)
    p5 = (40, 60)
    p6 = (210, 60)
    d.draw.polygon(display, c.COLORS['BLACK'], (p5, p6), 1)
    if card.cost < 10:
        draw_text(display, str(card.cost), (197, 40), c.COLORS['BLACK'], font_renderer)
    else:
        draw_text(display, str(card.cost), (193, 40), c.COLORS['BLACK'], font_renderer)
    if card.defp > 10 and card.atkp > 10:
        draw_text(display, str(card.atkp) + '/' + str(card.defp), (175, 280), c.COLORS['BLACK'], font_renderer)
    elif card.atkp > 10:
        draw_text(display, str(card.atkp) + '/' + str(card.defp), (180, 280), c.COLORS['BLACK'], font_renderer)
    elif card.defp > 10:
        draw_text(display, str(card.atkp) + '/' + str(card.defp), (180, 280), c.COLORS['BLACK'], font_renderer)
    else:
        draw_text(display, str(card.atkp) + '/' + str(card.defp), (190, 280), c.COLORS['BLACK'], font_renderer)



def handle_left_mouse_down(pos):
    if pos[u.X] >= 20 and pos[u.X] <= 80 and pos[u.Y] >= 20 and pos[u.Y] <= 50:
        print(pos)

d.init()
count = 0
display = d.display.set_mode((c.SCR_LEN, c.SCR_WID))
clock = d.time.Clock()
font_renderer = d.font.Font('font.ttf', c.FONT_SIZE)

while True:
    display.fill(c.BACKGROUND_COLOR)
    p = (m.floor(c.SCR_LEN / 2), 15)

    draw_card(display, font_renderer, tc.card('Warrior', 1, 1, 1, 'Creature'))
    # d.draw.polygon(display, c.COLORS['BLACK'], (p1, p2, p3, p4, p1), 1)
    # draw_text(display, 'Button', (27, 27), c.COLORS['BLACK'], font_renderer)

    for event in d.event.get():
        if event.type == d.QUIT:
            d.quit()
            quit()
        elif event.type == d.MOUSEBUTTONDOWN and event.button == u.LEFT:
            handle_left_mouse_down(event.pos)

    d.display.update()
    clock.tick(c.FPS)
