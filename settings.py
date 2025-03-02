import pyray as ray
import glm
from glm import vec2, vec3, ivec2, normalize, cross, dot, atan2, sin, cos, length

#Resolution
WIN_RES = WIN_WIDTH, WIN_HEIGHT = 1920, 1080

MAP_OFFSET = 50
MAP_WIDTH, MAP_HEIGHT = WIN_WIDTH - MAP_OFFSET, WIN_HEIGHT - MAP_OFFSET

EPS = 1e-4

#Camera
CAM_HEIGHT = 0.6
CAM_SPEED = 2.0
CAM_ROT_SPEED = 0.0015
CAM_DIAG_MOVE_CORR = 1 / pow(2, 0.5)

#Frustrum
FOV_Y_DEG = 50

#
VEC3_ZERO = ray.Vector3(0,0,0)
VEC3_ZERO = ray.Vector2(0,0)
#
WHITE_COLOR = ray.Color(255, 255, 255, 255)
BLACK_COLOR = ray.Color(0, 0, 0, 255)
DARK_GRAY_COLOR = ray.Color(80, 80, 80, 255)