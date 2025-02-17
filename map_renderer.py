from settings import *

class MapRenderer:
    def __init__(self, engine):
        self.engine = engine
        #
        raw_segments = [seg.pos for seg in self.engine.level_data.raw_segments]
        self.x_min, self.y_min, self.x_max, self.y_max = self.get_bounds(raw_segments)
        #
        self.raw_segments = self.remap_array(raw_segments)
        
    def draw(self):
        self.draw_raw_segments()
    
    def draw_normal(self, p0, p1, color, scale = 12):
        p10 = p1 - p0
        normal = normalize(vec2(-p10.y, p10.x))
        n0 = (p0 + p1) * 0.5
        n1 = n0 + normal * scale
        #
        ray.draw_line_v((n0.x, n0.y), (n1.x, n1.y), color)
    
    def draw_raw_segments(self):
        for p0, p1 in self.raw_segments:
            (x0, y0), (x1, y1) = p0, p1
            ray.draw_line_v((x0, y0), (x1, y1), ray.ORANGE)
            #
            self.draw_normal(p0, p1, ray.ORANGE)
            #
            ray.draw_circle_v((x0, y0), 3, ray.WHITE) 
    
    def remap_array(self, arr: list[vec2]):
        return [(self.remap_vec2(p0), self.remap_vec2(p1)) for p0, p1 in arr]
    
    def remap_vec2(self, p: vec2):
        x = self.remap_x(p.x)
        y = self.remap_y(p.y)
        return vec2(x, y)
    
    def remap_x(self, x, out_min = MAP_OFFSET, out_max = MAP_WIDTH):
        return (x - self.x_min) * (out_max - out_min) / (self.x_max - self.x_min) + out_min
    
    def remap_y(self, y, out_min = MAP_OFFSET, out_max = MAP_HEIGHT):
        return (y - self.y_min) * (out_max - out_min) / (self.y_max - self.y_min) + out_min
    
    @staticmethod
    def get_bounds(segments: list[tuple[vec2]]):
        inf = float('inf')
        x_min, y_min, x_max, y_max = inf, inf, -inf, -inf
        #
        for p0, p1 in segments:
            x_min = p0.x if p0.x < x_min else p1.x if p1.x < x_min else x_min
            x_max = p0.x if p0.x > x_max else p1.x if p1.x > x_max else x_max
            #
            y_min = p0.y if p0.y < y_min else p1.y if p1.y < y_min else y_min
            y_max = p0.y if p0.y > y_max else p1.y if p1.y > y_max else y_max
        return x_min, y_min, x_max, y_max  