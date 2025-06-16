import bpy
from bpy.types import PropertyGroup, UIList, Operator
from .base import BaseNode


class RenderPassItem(PropertyGroup):
    name: bpy.props.StringProperty(name="Name")


class SCENE_NODES_UL_render_passes(UIList):
    """UIList to display render passes."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)


class SCENE_NODES_OT_render_pass_add(Operator):
    bl_idname = "scene_nodes.render_pass_add"
    bl_label = "Add Render Pass"

    def execute(self, context):
        node = context.node
        node.passes.add()
        node.active_index = len(node.passes) - 1
        return {'FINISHED'}


class SCENE_NODES_OT_render_pass_remove(Operator):
    bl_idname = "scene_nodes.render_pass_remove"
    bl_label = "Remove Render Pass"

    def execute(self, context):
        node = context.node
        if node.passes and 0 <= node.active_index < len(node.passes):
            node.passes.remove(node.active_index)
            node.active_index = min(node.active_index, len(node.passes) - 1)
        return {'FINISHED'}


class RenderPassesNode(BaseNode):
    bl_idname = "RenderPassesNodeType"
    bl_label = "Render Passes"

    passes: bpy.props.CollectionProperty(type=RenderPassItem)
    active_index: bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        layout.template_list(
            "SCENE_NODES_UL_render_passes",
            "",
            self,
            "passes",
            self,
            "active_index",
        )
        row = layout.row(align=True)
        row.operator('scene_nodes.render_pass_add', text='', icon='ADD')
        row.operator('scene_nodes.render_pass_remove', text='', icon='REMOVE')
