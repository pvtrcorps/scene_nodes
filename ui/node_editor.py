import bpy
from bpy.types import Menu

class SCENE_GRAPH_MT_add(Menu):
    bl_label = "Add Scene Node"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_node", text="Scene Instance").type = "SceneInstanceNodeType"
        layout.operator("node.add_node", text="Transform").type = "TransformNodeType"
        layout.operator("node.add_node", text="Group").type = "GroupNodeType"
        layout.operator("node.add_node", text="Light").type = "LightNodeType"
        layout.operator("node.add_node", text="Global Options").type = "GlobalOptionsNodeType"
        layout.operator("node.add_node", text="Render Outputs").type = "OutputsStubNodeType"