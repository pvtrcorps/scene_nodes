import bpy

class SCENE_NODES_PT_node_props(bpy.types.Panel):
    bl_idname = "SCENE_NODES_PT_node_props"
    bl_label = "Node Properties"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node'

    @classmethod
    def poll(cls, context):
        node = context.active_node
        return node is not None and hasattr(node.__class__, "_prop_defs")

    def draw(self, context):
        node = context.active_node
        layout = self.layout
        for attr, label, _socket in getattr(node.__class__, '_prop_defs', []):
            prop_name = f"use_{attr}"
            if hasattr(node, prop_name):
                layout.prop(node, prop_name, text=label)


class SCENE_NODES_PT_node_props_properties(SCENE_NODES_PT_node_props):
    bl_idname = "SCENE_NODES_PT_node_props_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

def register():
    bpy.utils.register_class(SCENE_NODES_PT_node_props)
    bpy.utils.register_class(SCENE_NODES_PT_node_props_properties)


def unregister():
    bpy.utils.unregister_class(SCENE_NODES_PT_node_props_properties)
    bpy.utils.unregister_class(SCENE_NODES_PT_node_props)
