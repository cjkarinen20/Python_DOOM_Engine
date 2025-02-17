from settings import *

class Segment:
    def __init__(self, p0: tuple[float], p1: tuple[float]):
        #
        self.pos: tuple[float] = vec2(p0), vec2(p1)