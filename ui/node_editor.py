import bpy
from bpy.types import Menu

class SCENE_GRAPH_MT_add(Menu):
    bl_label = "Add Scene Node"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_node", text="Scene Instance").type = "SceneInstanceNodeType"
        layout.operator("node.add_node", text="Transform").type = "TransformNodeType"
        layout.operator("node.add_node", text="Input").type = "InputNodeType"
        layout.operator("node.add_node", text="Group").type = "GroupNodeType"
        layout.operator("node.add_node", text="Light").type = "LightNodeType"
        layout.operator("node.add_node", text="Global Options").type = "GlobalOptionsNodeType"
        layout.operator("node.add_node", text="Render Outputs").type = "OutputsStubNodeType"

def menu_draw(self, context):
    if context.space_data.tree_type == 'SceneNodeTreeType':
        self.layout.menu(SCENE_GRAPH_MT_add.bl_idname)


def register():
    bpy.types.NODE_MT_add.append(menu_draw)


def unregister():
    bpy.types.NODE_MT_add.remove(menu_draw)

