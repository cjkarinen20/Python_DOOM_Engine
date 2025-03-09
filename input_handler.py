from settings import *
from enum import IntEnum, auto
from pyray import is_key_down, is_key_pressed, KeyboardKey
import logging

logging.basicConfig(level=logging.INFO)

class Key(IntEnum):
    #
    FORWARD = KeyboardKey.KEY_W
    BACK = KeyboardKey.KEY_S
    STRAFE_LEFT = KeyboardKey.KEY_A
    STRAFE_RIGHT = KeyboardKey.KEY_D
    MAP = KeyboardKey.KEY_M
    JUMP = KeyboardKey.KEY_SPACE
    #
    
class InputHandler:
    def __init__(self, engine):
        self.engine = engine
        self.camera = engine.camera

    def update(self):
        #-------CAMERA MOVEMENT-------#
        if is_key_down(Key.FORWARD):
            logging.info("Moving forward")
            self.camera.step_forward()
        if is_key_down(Key.BACK):
            logging.info("Moving back")
            self.camera.step_back()
            self.camera.step_back()
        if is_key_down(Key.STRAFE_RIGHT):
            logging.info("Moving right")
            self.camera.step_right()
        if is_key_down(Key.STRAFE_LEFT):
            logging.info("Moving left")
            self.camera.step_left()
            self.camera.step_left()
        #------------MAP--------------#
        if is_key_pressed(Key.MAP):
            logging.info("Toggling map")
            self.engine.map_renderer.should_draw = not self.engine.map_renderer.should_draw
            self.engine.view_renderer.update_screen_tint()