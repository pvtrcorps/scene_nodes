import bpy
from .base import BaseNode, build_props_and_sockets


class OutputPropertiesNode(BaseNode):
    bl_idname = "OutputPropertiesNodeType"
    bl_label = "Output Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    OutputPropertiesNode,
    [
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
