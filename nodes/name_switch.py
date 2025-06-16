import bpy
from bpy.types import PropertyGroup, UIList, Operator
from .base import BaseNode


class NameSwitchItem(PropertyGroup):
    name: bpy.props.StringProperty(
        name="Name",
        update=lambda self, ctx: getattr(self.id_data, "update_sockets", lambda: None)(),
    )


class SCENE_NODES_UL_name_switch(UIList):
    """UIList to display switch inputs."""

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "name", text="", emboss=False)


class SCENE_NODES_OT_name_switch_add(Operator):
    bl_idname = "scene_nodes.name_switch_add"
    bl_label = "Add Input"

    def execute(self, context):
        node = context.node
        node.names.add()
        node.active_index = len(node.names) - 1
        node.update_sockets()
        return {'FINISHED'}


class SCENE_NODES_OT_name_switch_remove(Operator):
    bl_idname = "scene_nodes.name_switch_remove"
    bl_label = "Remove Input"

    def execute(self, context):
        node = context.node
        if node.names and 0 <= node.active_index < len(node.names):
            node.names.remove(node.active_index)
            node.active_index = min(node.active_index, len(node.names) - 1)
            node.update_sockets()
        return {'FINISHED'}


class NameSwitchNode(BaseNode):
    bl_idname = "NameSwitchNodeType"
    bl_label = "Name Switch"

    names: bpy.props.CollectionProperty(type=NameSwitchItem)
    active_index: bpy.props.IntProperty()

    def init(self, context):
        self.inputs.new('SceneSocketType', "Default")
        self.update_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def update_sockets(self):
        existing = {
            sock.name: sock
            for sock in self.inputs
            if sock.bl_idname == 'SceneSocketType' and sock.name != 'Default'
        }
        for item in self.names:
            if item.name in existing:
                existing.pop(item.name)
            else:
                self.inputs.new('SceneSocketType', item.name)
        for sock in existing.values():
            self.inputs.remove(sock)

    def draw_buttons(self, context, layout):
        layout.template_list(
            "SCENE_NODES_UL_name_switch",
            "",
            self,
            "names",
            self,
            "active_index",
        )
        row = layout.row(align=True)
        row.operator('scene_nodes.name_switch_add', text='', icon='ADD')
        row.operator('scene_nodes.name_switch_remove', text='', icon='REMOVE')

