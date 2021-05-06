#!/usr/bin/env python
#from manimlib.imports import *
from manim import *


RAD = 0.4

#https://algorithmtutor.com/Data-Structures/Tree/Red-Black-Trees/

#base scene for all tree scenes
class firstTreeScenes(Scene):

    def __init__(self, **kwargs):
        Scene.__init__(self, **kwargs)

    def construct(self):
        pass
        

class test(firstTreeScenes):
    def construct(self):

        dot1 = Circle(radius = RAD, color = BLACK, stroke_color = WHITE)
        dot2 = Circle(radius = RAD, color = BLACK, stroke_color = WHITE)
        dot3 = Circle(radius = RAD, color = RED, stroke_color = RED)
        line = always_redraw(lambda: Line(dot1.get_center(), dot2.get_center(), buff=RAD))
        self.add(line)
        dot1.to_edge(LEFT)
        dot2.to_edge(RIGHT)
        self.play(dot1.animate.move_to(UP*3))

        line.suspend_updating()
        #dot1 = dot3
        self.play(Transform(dot1, dot3))

        self.play(dot2.animate.move_to(UP*3))     

        self.wait(3)

class test2(firstTreeScenes):
    def construct(self):
        val = 55
        val2 = "prova"
        testo = Tex(str(val), color = WHITE)
        testo2 = Tex(str(val2), color = WHITE)

        self.add(testo)  
        self.wait(3)
        self.play(Transform(testo, testo2))   

        self.wait(3)