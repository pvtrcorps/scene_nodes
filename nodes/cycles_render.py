import bpy
from .base import BaseNode, build_props_and_sockets


class CyclesRenderNode(BaseNode):
    bl_idname = "CyclesRenderNodeType"
    bl_label = "Cycles Render Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    CyclesRenderNode,
    [
        ("samples", "int", {"name": "Samples", "default": 128}),
        ("use_denoise", "bool", {"name": "Use Denoise", "default": False}),
    ],
)
