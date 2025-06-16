import bpy
from .base import BaseNode, build_props_and_sockets

class TransformNode(BaseNode):
    bl_idname = "TransformNodeType"
    bl_label = "Transform"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    TransformNode,
    [
        ("translate", "vector", {"name": "Translate", "size": 3}),
        ("rotate", "vector", {"name": "Rotate", "size": 3}),
        ("scale", "vector", {"name": "Scale", "size": 3, "default": (1, 1, 1)}),
        ("filter_expr", "string", {"name": "Filter"}),
    ],
)
