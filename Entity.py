#!/usr/bin/env python
# -*- coding: utf-8 -*-
import utils as u
import config as c
import random as r


class Entity:

    def __init__(self, pos, name, sens, spd, color, size, gender, dir):
        self.pos = pos
        self.name = name
        self.sens = sens
        self.spd = spd
        self.color = color
        self.size = size
        self.gender = gender
        self.dir = dir
        self.env_data = []

    def __str__(self):
        text = self.name + self.gender

        return text

    def get_polygon(self, pos):
        p1 = u.calc_point(self.dir, self.size, pos)
        p2 = u.calc_point(self.dir - 150, self.size * 1.6, p1)
        p3 = u.calc_point(self.dir + 150, self.size * 1.6, p1)

        return (pos, p3, p1, p2, pos)

    def get_sens_polygon(self, pos):
        xl1 = pos[u.X] - self.sens
        xl2 = pos[u.X] + self.sens
        yl1 = pos[u.Y] - self.sens
        yl2 = pos[u.Y] + self.sens

        p1 = (xl1, yl1)
        p2 = (xl1, yl2)
        p3 = (xl2, yl2)
        p4 = (xl2, yl1)

        return (p1, p2, p3, p4, p1)

    def move(self, p=None):
        if p is not None:
            d = u.calc_distance(self.pos, p)
            if d < self.spd:
                self.pos = p
                return True
            else:
                self.dir = u.calc_θ(self.pos, p)
                self.pos = u.calc_point(self.dir, self.spd, self.pos)
                return True
        else:
            p = u.calc_point(self.dir, self.spd, self.pos)
            if u.is_point_within_rect(c.MAP_LEN, c.MAP_WID, p):
                self.pos = p
                return True
            else:
                return False

    def think(self):
        p = u.calc_point(self.dir, self.spd, self.pos)
        while not u.is_point_within_rect(c.MAP_LEN, c.MAP_WID, p):
            self.dir = r.randint(0, 360)
            p = u.calc_point(self.dir, self.spd, self.pos)

    def forget(self, surr_resources):
        surr_memories = []

        for resource in self.env_data:
            if u.is_point_within_sqr(self.pos, self.sens, resource.pos):
                surr_memories.append(resource)

        for resource in surr_memories:
            if resource not in surr_resources:
                self.env_data.remove(resource)

    def do(self, status):
        surr_resources = []

        for resource in status['resources']:
            if u.is_point_within_sqr(self.pos, self.sens, resource.pos):
                surr_resources.append(resource)
                if resource not in self.env_data:
                    self.env_data.append(resource)

        self.forget(surr_resources)

        """for i in range(1, self.spd + 1):
            p = u.calc_point(self.dir, i, self.pos)
            if u.is_point_in_line(status['env'][0][0], status['env'][0][1], p):
                print('collision')"""

        if surr_resources:
            t_resource = None
            min_d = c.MAP_LEN + c.MAP_WID

            for resource in surr_resources:
                d = u.calc_distance(self.pos, resource.pos)
                if d < min_d:
                    min_d = d
                    t_resource = resource

            self.move(t_resource.pos)

            if t_resource.pos == self.pos:
                status['resources'].remove(t_resource)
                if t_resource in self.env_data:
                    self.env_data.remove(t_resource)
        else:
            self.think()
            self.move()
