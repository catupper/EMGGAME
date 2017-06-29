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

def contrast(color, q, p):
    r,g,b = color
    return (r*q/p, g*q/p, b*q/p)
    

class Game:
    def __init__(self):
        self.WIDTH = 1500
        self.HEIGHT = 800
        self.SQW = 40
        self.SQH = 30
        self.SQD = 200 #D
        self.SQC = WHITE #C
        self.SQT = self.HEIGHT / 2
        self.TRIAL = 25
        self.DISPLAYTIME = 0.1 #sec
        self.clock = pygame.time.Clock()
        self.contrast = 1
        self.lr = 1
        pygame.init()
        pygame.display.set_caption("CognitiveGame")
        self.screen = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        self.font = pygame.font.Font(None, 80)
        self.clock = pygame.time.Clock()
        self.state = "START"
        self.BACKGROUND_COLOR = BLACK
        self.rect = [pygame.Surface((self.SQW, self.SQH)) for i in range(16)]
        self.centerpoint = pygame.Surface((6,6))
        pygame.draw.circle(self.centerpoint, WHITE, (3,3), 3)
        for i in range(16):
            s = self.rect[i]
            s.fill(contrast(self.SQC, i+1, 16))                   
        self.nrect = None
        self.log = []

    def save_result(self):
        print self.log

    def checkQUIT(self, events):
        for event in events:
            if event.type == QUIT:
                return True
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                return True
        return False

    def set_rect(self):
        x = self.WIDTH / 2
        self.lr = "LR"[random.randint(0,1)]
        if self.lr == "R":
            x += self.SQD - self.SQW / 2

        if self.lr == "L":
            x -= self.SQD + self.SQW / 2
        print x - self.WIDTH/2
        self.contrast = random.randint(0, 15)
        self.nrect = (self.rect[self.contrast], (x, self.SQT))

    def draw_center_circle(self):
        self.screen.blit(self.centerpoint, (self.WIDTH / 2 - 3, 10 + self.HEIGHT / 2 - 3))
        
    def next_rect(self):
        return self.nrect
    
    def start_run(self, events):
        self.screen.fill(self.BACKGROUND_COLOR)
        ren = self.font.render("Press Any Key!", 0, WHITE, BLACK)
        self.screen.blit(ren, (10, 10))
        pygame.display.flip()
        for event in events:
            if event.type == KEYUP:
                return "PLAYWAIT"
        return "START"

    def set_time(self):
        self.timestamp = time.time()

    def get_time(self):
        return time.time() - self.timestamp
        
    def play_wait(self, events):
        if self.TRIAL == 0:
            return "END"
        self.screen.fill(self.BACKGROUND_COLOR)                     
        ren = self.font.render("Press SpaceBar", 0, WHITE, BLACK)
        self.screen.blit(ren, (10, 10))
        self.draw_center_circle()
        pygame.display.flip()
        for event in events:
            if event.type == KEYDOWN and event.key == K_SPACE:
                self.TRIAL -= 1
                self.set_time()
                self.set_rect()
                return "PLAYDISPLAY"
        return "PLAYWAIT"

    def play_display(self, events):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.screen.blit(*self.next_rect())
        self.draw_center_circle()
        pygame.display.flip()
        if self.get_time() > self.DISPLAYTIME:
            self.set_time()
            return "PLAYASK"
        return "PLAYDISPLAY"

    def add_log(self, result):
        self.log.append(
            [self.get_time(),
             self.contrast,
             self.lr,
             result
            ])
        
    
    def play_ask(self, events):
        self.screen.fill(self.BACKGROUND_COLOR)                     
        ren = self.font.render("L or R?", 0, WHITE, BLACK)
        self.screen.blit(ren, (10, 10))
        self.draw_center_circle()
        pygame.display.flip()
        for event in events:
            if event.type == KEYDOWN and event.key == K_LEFT:
                self.add_log("L")
                return "PLAYWAIT"
            if event.type == KEYDOWN and event.key == K_RIGHT:
                self.add_log("R")
                return "PLAYWAIT"
        return "PLAYASK"
    
    def _run(self):
        events = pygame.event.get()
        if self.checkQUIT(events):return "STOP"
        
        if self.state == "START":
            return self.start_run(events)
        if self.state == "PLAYWAIT":
            return self.play_wait(events)
        if self.state == "PLAYDISPLAY":
            return self.play_display(events)
        if self.state == "PLAYASK":
            return self.play_ask(events)
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
