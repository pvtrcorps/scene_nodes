import bpy
from .base import BaseNode, build_props_and_sockets


class EeveeRenderNode(BaseNode):
    bl_idname = "EeveeRenderNodeType"
    bl_label = "Eevee Render Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    EeveeRenderNode,
    [
        ("samples", "int", {"name": "Samples", "default": 64}),
        ("use_bloom", "bool", {"name": "Bloom", "default": False}),
    ],
)
