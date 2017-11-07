#!/usr/bin/python
# -*- coding: UTF-8 -*-

from collections import Generator
import random

class Agent(Generator):
    
    def __init__(self, kb, name):
        self.name = name
        self.kb = kb

    def send(self, msg):
            
        ###
        ### Generate answer...
        ###

        return random.choice(self.kb.values)[0]

    def throw(self, typ=None, val=None, tb=None):
        # Оставляем как есть
        super().throw(typ, val, tb)

    def __str__(self):
        head = 5
        return "Name {0}".format(self.name) + "answers:" + "\n".join(list(*zip(*self.kb.values[:head])))

    def __repr__(self):
        return 'Agent({0})'.format(self.name)
