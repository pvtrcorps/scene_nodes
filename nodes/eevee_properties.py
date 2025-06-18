import bpy
from .base import BaseNode, build_props_and_sockets


class EeveePropertiesNode(BaseNode):
    bl_idname = "EeveePropertiesNodeType"
    bl_label = "Eevee Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    EeveePropertiesNode,
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
        ("use_taa_reprojection", "bool", {"name": "TAA Reprojection"}),

        # Clamping
        ("clamp_direct", "float", {"name": "Clamp Direct", "default": 0.0}),
        ("clamp_indirect", "float", {"name": "Clamp Indirect", "default": 0.0}),

        # Raytracing
        ("raytrace_resolution", "int", {"name": "Raytrace Resolution", "default": 512}),

        # Motion Blur
        ("motion_blur", "bool", {"name": "Motion Blur"}),
        ("motion_blur_shutter", "float", {"name": "Shutter", "default": 0.5}),

        # Film
        ("film_exposure", "float", {"name": "Exposure", "default": 1.0}),
    ],
)
