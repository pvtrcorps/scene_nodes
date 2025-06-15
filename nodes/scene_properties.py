import bpy
from .base import BaseNode
from .property_utils import build_node_from_rna

class ScenePropertiesNode(BaseNode):
    bl_idname = "ScenePropertiesNodeType"
    bl_label = "Scene Properties"
    property_group_path = []

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_node_from_rna(ScenePropertiesNode, bpy.types.Scene)
