import bpy
from .base import BaseNode, build_props_and_sockets


class ScenePropertiesNode(BaseNode):
    bl_idname = "ScenePropertiesNodeType"
    bl_label = "Scene Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    ScenePropertiesNode,
    [
        ("res_x", "int", {"name": "Resolution X", "default": 1920}),
        ("res_y", "int", {"name": "Resolution Y", "default": 1080}),
        ("camera_path", "string", {"name": "Camera Path"}),
    ],
)
