from settings import *
from models import Models


class ViewRenderer:
    def __init__(self, engine):
        self.engine = engine
        #
        self.segments = engine.bsp_builder.segments
        self.camera = engine.camera
        self.segment_ids_to_draw = self.engine.bsp_traverser.seg_ids_to_draw
        #
        self.models = Models(engine)
        self.wall_models = self.models.wall_models
        #
        self.wall_ids_to_draw = set()
        #
        self.screen_tint = WHITE_COLOR

    def update(self):
        self.wall_ids_to_draw.clear()

        for seg_id in self.segment_ids_to_draw:
            # walls
            seg = self.segments[seg_id]
            self.wall_ids_to_draw |= seg.wall_model_id

    def draw(self):
        # draw walls
        for wall_id in self.wall_ids_to_draw:
            ray.draw_model(self.wall_models[wall_id], VEC3_ZERO, 1.0, self.screen_tint)

    def update_screen_tint(self):
        self.screen_tint = (
            DARK_GRAY_COLOR if self.engine.map_renderer.is_draw_map else WHITE_COLOR
        )
