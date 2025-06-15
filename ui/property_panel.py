import bpy
from bpy.types import Panel
from ..nodes.base import BaseNode


class SCENE_GRAPH_PT_property_sockets(Panel):
    bl_idname = "SCENE_GRAPH_PT_property_sockets"
    bl_label = "Node Properties"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Scene Nodes'

    @classmethod
    def poll(cls, context):
        node = context.active_node
        return isinstance(node, BaseNode)

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        for attr, label, _sid in getattr(node.__class__, '_prop_defs', []):
            prop_name = f"use_{attr}"
            if hasattr(node, prop_name):
                layout.prop(node, prop_name, text=label)
