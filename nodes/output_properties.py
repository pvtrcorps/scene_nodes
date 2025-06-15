import bpy
from .base import BaseNode
from .property_utils import build_node_from_rna

class OutputPropertiesNode(BaseNode):
    bl_idname = "OutputPropertiesNodeType"
    bl_label = "Output Properties"
    property_group_path = ["render"]

    def init(self, context):
        super().init(context)
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_node_from_rna(OutputPropertiesNode, bpy.types.RenderSettings)
