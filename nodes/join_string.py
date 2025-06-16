import bpy
from .base import BaseNode, build_props_and_sockets


class JoinStringNode(BaseNode):
    bl_idname = "JoinStringNodeType"
    bl_label = "Join String"

    def init(self, context):
        self.add_enabled_sockets()
        self.outputs.new('StringSocketType', "String")

    def draw_buttons(self, context, layout):
        pass


build_props_and_sockets(
    JoinStringNode,
    [
        ("string1", "string", {"name": "String 1"}),
        ("string2", "string", {"name": "String 2"}),
        ("delimiter", "string", {"name": "Delimiter"}),
    ],
)
