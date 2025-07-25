import bpy
from bpy.types import Menu

class SCENE_GRAPH_MT_add(Menu):
    bl_idname = "SCENE_GRAPH_MT_add"
    bl_label = "Add Scene Node"

    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_node", text="Blend Input").type = "BlendInputNodeType"
        layout.operator("node.add_node", text="Transform").type = "TransformNodeType"
        layout.operator("node.add_node", text="Input").type = "InputNodeType"
        layout.operator("node.add_node", text="Join String").type = "JoinStringNodeType"
        layout.operator("node.add_node", text="Split String").type = "SplitStringNodeType"
        layout.operator("node.add_node", text="Name Switch").type = "NameSwitchNodeType"
        layout.operator("node.add_node", text="Group").type = "GroupNodeType"
        layout.operator("node.add_node", text="Light").type = "LightNodeType"
        layout.operator("node.add_node", text="Global Options").type = "GlobalOptionsNodeType"
        layout.operator("node.add_node", text="Render Passes").type = "RenderPassesNodeType"
        layout.operator("node.add_node", text="Scene Properties").type = "ScenePropertiesNodeType"
        layout.operator("node.add_node", text="Render Properties").type = "RenderPropertiesNodeType"
        layout.operator("node.add_node", text="Output Properties").type = "OutputPropertiesNodeType"
        layout.operator("node.add_node", text="Render Engine").type = "RenderEngineNodeType"
        layout.operator("node.add_node", text="Eevee Attributes").type = "EeveeAttributesNodeType"
        layout.operator("node.add_node", text="Render").type = "RenderNodeType"

def menu_draw(self, context):
    if context.space_data.tree_type == 'SceneNodeTreeType':
        self.layout.menu(SCENE_GRAPH_MT_add.bl_idname)


def register():
    bpy.types.NODE_MT_add.append(menu_draw)


def unregister():
    bpy.types.NODE_MT_add.remove(menu_draw)

