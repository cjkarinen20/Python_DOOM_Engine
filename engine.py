from settings import *
from level_data import LevelData
from map_renderer import MapRenderer


class Engine:
    def __init__(self, app):
        self.app = app
        #
        self.level_data = LevelData(self)
        self.map_renderer = MapRenderer(self)
    
    def update(self):
        pass
    
    def draw_2d(self):
        self.map_renderer.draw()
    
    def draw_3d(self):
        pass
    
    def draw(self):
        ray.begin_drawing()
        #
        ray.clear_background(ray.BLACK)
        self.draw_3d()
        self.draw_2d()
        #
        ray.end_drawing()
        
        