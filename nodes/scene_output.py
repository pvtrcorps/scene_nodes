import bpy
from .base import BaseNode, build_props_and_sockets


class SceneOutputNode(BaseNode):
    bl_idname = "SceneOutputNodeType"
    bl_label = "Scene Output"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    SceneOutputNode,
    [
        ("scene_name", "string", {"name": "Name"}),
    ],
)
