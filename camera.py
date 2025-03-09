from settings import *

def ease_out_cubic(t):
    return 1 - pow(1 - t, 3)

class Camera:
    def __init__(self, engine):
        self.app = engine.app
        self.engine = engine
        #
        self.fake_up = vec3(0.0, 1.0, 0.0)
        #
        self.m_cam: ray.Camera3D = self.get_camera()
        #
        self.target: ray.Vector3 = self.m_cam.target
        self.pos_3d: ray.Vector3 = self.m_cam.position
        self.pos_2d: glm.vec2 = vec2(self.pos_3d.x, self.pos_3d.z)
        #
        self.speed = CAM_SPEED
        self.cam_step = vec3(0)
        #
        self.forward = vec3(0)
        self.right = vec3(0)
        #
        self.yaw = atan2(self.target.z - self.pos_3d.z, self.target.x - self.pos_3d.x)
        self.pitch = 0.0
        self.delta_yaw = 0.0
        self.delta_pitch = 0.0
        #
        self.jump_velocity = 0.0
        self.is_jumping = False
        self.gravity = GRAVITY
        self.jump_start_height = JUMP_START_POS
        self.jump_duration = JUMP_DURATION
        
    def get_yaw_pitch(self):
        mouse_delta = ray.get_mouse_delta()
        self.delta_yaw = -mouse_delta.x * CAM_ROT_SPEED * CAM_SENSITIVITY * self.app.dt
        self.delta_pitch = -mouse_delta.y * CAM_ROT_SPEED * CAM_SENSITIVITY * self.app.dt
        #Update yaw
        self.yaw -= self.delta_yaw
        #Update pitch and clamp it
        self.pitch = max(min(self.pitch + self.delta_pitch, CAM_PITCH_LIMIT), -CAM_PITCH_LIMIT) 
        
    def set_yaw_pitch(self):
        self.get_yaw_pitch()
        #
        front = vec3(
            cos(radians(self.yaw)) * cos(radians(self.pitch)),
            sin(radians(self.pitch)),
            sin(radians(self.yaw)) * cos(radians(self.pitch))
        )
        new_target_pos = glm.normalize(front)
        self.update_target(new_target_pos)
        
    def update_target(self, new_target_pos: vec3):
        self.target.y = self.pos_3d.y + new_target_pos.y
        self.target.x = self.pos_3d.x + new_target_pos.x
        self.target.z = self.pos_3d.z + new_target_pos.z

    def pre_update(self):
        self.init_cam_step()
        self.update_vectors()

    def update(self):
        self.check_cam_step()
        self.update_pos_2d()
        self.set_yaw_pitch()
        self.move()
        self.apply_gravity()
        
    def apply_gravity(self):
        if self.is_jumping:
            self.jump_velocity += self.gravity * self.app.dt
            self.jump_duration += self.app.dt
            #
            t = JUMP_DURATION
            eased_t = ease_out_cubic(t)
            #
            self.pos_3d.y = self.jump_start_height + self.jump_velocity * eased_t * self.app.dt
            self.target.y = self.pos_3d.y
            #
            if self.pos_3d.y <= CAM_HEIGHT: #Ground check
                self.target.y = CAM_HEIGHT
                self.is_jumping = False
                self.jump_velocity = 0.0
                self.jump_duration = 0.0
        else:
            if ray.is_key_pressed(ray.KEY_SPACE):
                self.is_jumping = True
                self.jump_velocity = JUMP_VELOCITY
                self.jump_start_height = self.pos_3d.y
                self.jump_duration = 0.0
                

    def update_vectors(self):
        self.forward = self.get_forward()
        self.right = cross(self.forward, self.fake_up)

    def get_forward(self) -> glm.vec3:
        return normalize(vec3(
            self.target.x - self.pos_3d.x,
            self.target.y - self.pos_3d.y,
            self.target.z - self.pos_3d.z,
        ))

    def init_cam_step(self):
        self.speed = CAM_SPEED * self.app.dt
        self.cam_step *= 0

    def step_forward(self):
        self.cam_step += self.speed * self.forward

    def step_back(self):
        self.cam_step += -self.speed * self.forward

    def step_left(self):
        self.cam_step += -self.speed * self.right

    def step_right(self):
        self.cam_step += self.speed * self.right

    def check_cam_step(self):
        dx, dz = self.cam_step.xz
        if dx and dz:
            self.cam_step *= CAM_DIAG_MOVE_CORR

    def move(self):
        dx, dz = self.cam_step.xz
        self.move_x(dx)
        self.move_z(dz)

    def move_x(self, dx):
        self.pos_3d.x += dx
        self.target.x += dx

    def move_z(self, dz):
        self.pos_3d.z += dz
        self.target.z += dz

    def update_pos_2d(self):
        # 2d position on xz plane
        self.pos_2d[0] = self.pos_3d.x
        self.pos_2d[1] = self.pos_3d.z

    def get_camera(self):
        cam = ray.Camera3D(
            self.engine.level_data.settings['cam_pos'],
            self.engine.level_data.settings['cam_target'],
            self.fake_up.to_tuple(),
            FOV_Y_DEG,
            ray.CAMERA_PERSPECTIVE
        )
        return cam
