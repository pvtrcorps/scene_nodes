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
        ("res_x", "int", {"name": "Resolution X", "default": 1920}),
        ("res_y", "int", {"name": "Resolution Y", "default": 1080}),
        ("frame_start", "int", {"name": "Frame Start", "default": 1}),
        ("frame_end", "int", {"name": "Frame End", "default": 250}),
        ("fps", "int", {"name": "FPS", "default": 24}),
        ("camera_path", "string", {"name": "Camera Path"}),
        ("samples", "int", {"name": "Samples", "default": 64}),
        ("motion_blur", "bool", {"name": "Motion Blur"}),
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
    ],
)
