import bpy
from .base import BaseNode, build_props_and_sockets


class CyclesPropertiesNode(BaseNode):
    bl_idname = "CyclesPropertiesNodeType"
    bl_label = "Cycles Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    CyclesPropertiesNode,
    [
        # General Output
        ("res_x", "int", {"name": "Resolution X", "default": 1920}),
        ("res_y", "int", {"name": "Resolution Y", "default": 1080}),
        ("frame_start", "int", {"name": "Frame Start", "default": 1}),
        ("frame_end", "int", {"name": "Frame End", "default": 250}),
        ("fps", "int", {"name": "FPS", "default": 24}),
        ("camera_path", "string", {"name": "Camera Path"}),
        ("filepath", "string", {"name": "File Path", "subtype": "FILE_PATH"}),
        (
            "file_format",
            "enum",
            {
                "items": [
                    ("OPEN_EXR", "OpenEXR", ""),
                    ("PNG", "PNG", ""),
                ],
                "name": "Format",
            },
        ),
        (
            "color_mode",
            "enum",
            {
                "name": "Color",
                "items": [
                    ("BW", "BW", ""),
                    ("RGB", "RGB", ""),
                    ("RGBA", "RGBA", ""),
                ],
                "default": "RGB",
            },
        ),

        # Sampling
        ("samples", "int", {"name": "Samples", "default": 64}),
        ("use_adaptive_sampling", "bool", {"name": "Adaptive Sampling"}),

        # Light Paths
        ("max_bounces", "int", {"name": "Max Bounces", "default": 8}),
        ("diffuse_bounces", "int", {"name": "Diffuse Bounces", "default": 4}),

        # Volumes
        ("volume_step_rate", "float", {"name": "Volume Step Rate", "default": 1.0}),

        # Curves
        ("hair_shape_radius", "float", {"name": "Hair Shape Radius", "default": 1.0}),

        # Simplify
        ("use_simplify", "bool", {"name": "Use Simplify"}),

        # Motion Blur
        ("motion_blur_shutter", "float", {"name": "Shutter", "default": 0.5}),

        # Film
        ("film_exposure", "float", {"name": "Exposure", "default": 1.0}),

        # Performance
        ("tile_x", "int", {"name": "Tile X", "default": 64}),

        # Grease Pencil
        ("gpencil_antialias_threshold", "float", {"name": "Grease Pencil AA", "default": 1.0}),

        # Freestyle
        ("use_freestyle", "bool", {"name": "Use Freestyle"}),
    ],
)
