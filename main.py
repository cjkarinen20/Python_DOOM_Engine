from settings import *
from engine import Engine

class App:
    ray.set_trace_log_level(ray.LOG_ERROR)
    ray.init_window(WIN_WIDTH, WIN_HEIGHT, 'BSP Engine')
    
    def __init__(self):
        self.dt = 0.0 
        self.engine = Engine(app = self)
        
    def run(self):
        while not ray.window_should_close():
            self.dt = ray.get_frame_time()
            self.engine.update()
            self.engine.draw()
        #
        ray.close_window()
        
if __name__ == '__main__':
    app = App()
    app.run()