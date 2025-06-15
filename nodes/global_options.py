import bpy
from .base import BaseNode, build_props_and_sockets

class GlobalOptionsNode(BaseNode):
    bl_idname = "GlobalOptionsNodeType"
    bl_label = "Global Options"

    def init(self, context):
        super().init(context)
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    GlobalOptionsNode,
    [
        ("res_x", "int", {"name": "Resolution X", "default": 1920}),
        ("res_y", "int", {"name": "Resolution Y", "default": 1080}),
        ("samples", "int", {"name": "Samples", "default": 128}),
        ("camera_path", "string", {"name": "Camera Path"}),
    ],
)
