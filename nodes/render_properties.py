import bpy
from .base import BaseNode
from .property_utils import build_node_from_rna

class RenderCyclesNode(BaseNode):
    bl_idname = "RenderCyclesNodeType"
    bl_label = "Render Properties Cycles"
    property_group_path = ["cycles"]

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_node_from_rna(RenderCyclesNode, bpy.types.CyclesRenderSettings)


class RenderEeveeNode(BaseNode):
    bl_idname = "RenderEeveeNodeType"
    bl_label = "Render Properties EEVEE"
    property_group_path = ["eevee"]

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass


build_node_from_rna(RenderEeveeNode, bpy.types.EeveeRenderSettings if hasattr(bpy.types, 'EeveeRenderSettings') else bpy.types.Scene.eevee.__class__)
