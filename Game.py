#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pygame, random
import sys, time
from pygame.locals import *


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
EPS = 1e-7

def contrast(color, q, p, color2 = (0,0,0)):
    r,g,b = color
    r1,g1,b1 = color2
    return (r1 + (r-r1)*q/p, g1 + (g-g1)*q/p, b1 + (b-b1)*q/p)
    

class Game:
    def __init__(self):
        self.WIDTH = 1500
        self.HEIGHT = 800
        self.SQW = 40
        self.SQH = 30
        self.SQD = 500 #D
        self.SQC = WHITE #C
        self.SQT = self.HEIGHT / 2
        self.TRIAL = 5
        self.DISPLAYTIME = 0.1#sec
        self.clock = pygame.time.Clock()
        self.contrast = 1
        self.lr = 1
        self.x = self.WIDTH / 2
        self.vx = 5
        self.a = 3
        self.R = 30
        self.y = self.HEIGHT / 2 + 20
        self.LEDGE = self.WIDTH / 2 - self.SQD  - self.R 
        self.REDGE = self.WIDTH / 2 + self.SQD  - self.R
        pygame.init()
        pygame.display.set_caption("CognitiveGame")
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font = pygame.font.Font(None, 80)
        self.clock = pygame.time.Clock()
        self.state = "START"
        self.BACKGROUND_COLOR = BLACK
        self.rect = [pygame.Surface((self.SQW, self.SQH)) for i in range(16)]
        self.circle = pygame.Surface((self.R*2,self.R*2))
        self.circle.fill(contrast(WHITE, 1, 1.0))
        #pygame.draw.circle(self.circle, WHITE, (self.R, self.R), self.R)
        for i in range(16):
            s = self.rect[i]
            s.fill(contrast(self.SQC, i+1, 16))                   
        self.nrect = None
        self.log = []

    def save_result(self):
        print "%6s  %10s  %10s  %10s"%("Time(sec)", "contrast", "correct", "result")
        for log in self.log:
            print "%.5lf, %10d, %10c, %10c"%tuple(log)

    def checkQUIT(self, events):
        for event in events:
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
        return False
    
    def start_run(self, events):
        self.screen.fill(self.BACKGROUND_COLOR)
        ren = self.font.render("Press Any Key!", 0, WHITE, BLACK)
        self.screen.blit(ren, (10, 10))
        pygame.display.flip()
        for event in events:
            if event.type == KEYUP:
                self.set_time()
                return "MOVE"
        return "START"

    def set_time(self):
        self.timestamp = time.time()

    def get_time(self):
        return time.time() - self.timestamp

    def move(self):
        self.x += self.vx
        print self.x, self.LEDGE, self.REDGE
        if self.x < self.LEDGE or self.x > self.REDGE:
            self.vx *= -1

    def speed_up(self):
        self.circle.fill(contrast(WHITE, self.contrast, 1.0, RED))
        self.contrast -= 0.1
        if(self.vx > 0):self.vx += self.a
        else :self.vx -= self.a
            
    def move_run(self, events):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.screen.blit(self.circle, (self.x, self.y))
        self.move()
        pygame.display.flip()
        if(self.get_time() > 5):
            self.speed_up()
            self.set_time()
        if self.vx > 100:
            return "START"
        return "MOVE"

    def add_log(self, result):
        self.log.append(
            [self.get_time(),
             self.contrast,
             self.lr,
             result
            ])
        
    def _run(self):
        events = pygame.event.get()
        if self.checkQUIT(events):return "STOP"
        
        if self.state == "START":
            return self.start_run(events)
        if self.state == "MOVE":
            return self.move_run(events)
        return "STOP"

    
    def run(self):
        while True:
            self.clock.tick(60)
            self.state = self._run()
            if self.state == "STOP":
                break

        self.save_result()
            
    
def main():
    game = Game()
    game.run()
    
if __name__ == "__main__":
    main()
