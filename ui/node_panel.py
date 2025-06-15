import bpy

class SCENE_NODES_PT_node_props(bpy.types.Panel):
    bl_idname = "SCENE_NODES_PT_node_props"
    bl_label = "Node Properties"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Item'

    @classmethod
    def poll(cls, context):
        space = context.space_data
        return (
            space is not None
            and space.tree_type == 'SceneNodeTreeType'
            and context.active_node is not None
        )

    def draw(self, context):
        node = context.active_node
        layout = self.layout
        for attr, label, _socket in getattr(node.__class__, '_prop_defs', []):
            prop_name = f"use_{attr}"
            if hasattr(node, prop_name):
                layout.prop(node, prop_name, text=label)

def register():
    bpy.utils.register_class(SCENE_NODES_PT_node_props)


def unregister():
    bpy.utils.unregister_class(SCENE_NODES_PT_node_props)
