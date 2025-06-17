import bpy
from .base import BaseNode, build_props_and_sockets


class RenderNode(BaseNode):
    bl_idname = "RenderNodeType"
    bl_label = "Render"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    RenderNode,
    [
        ("scene_name", "string", {"name": "Name"}),
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
    ],
)
