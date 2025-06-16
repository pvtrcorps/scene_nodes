import bpy
from .base import BaseNode, build_props_and_sockets


class SplitStringNode(BaseNode):
    bl_idname = "SplitStringNodeType"
    bl_label = "Split String"

    def init(self, context):
        self.add_enabled_sockets()
        self.outputs.new('StringSocketType', "Part 1")
        self.outputs.new('StringSocketType', "Part 2")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    SplitStringNode,
    [
        ("string", "string", {"name": "String"}),
        ("separator", "string", {"name": "Separator"}),
    ],
)
