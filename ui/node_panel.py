import bpy

class SCENE_GRAPH_PT_node_properties(bpy.types.Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node'
    bl_label = 'Scene Node'

    @classmethod
    def poll(cls, context):
        node = getattr(context, 'active_node', None)
        return node is not None and hasattr(node, 'update_sockets')

    def draw(self, context):
        layout = self.layout
        node = context.active_node
        cls = node.__class__
        if getattr(cls, '_prop_defs', []):
            for attr, label, _socket in getattr(cls, '_prop_defs', []):
                row = layout.row()
                row.prop(node, attr, text=label)
                expose = cls._expose_prop_map.get(attr)
                if expose:
                    row.prop(node, expose, text='Socket')
        else:
            if hasattr(node, 'data_type'):
                layout.prop(node, 'data_type')
                if node.data_type == 'FLOAT':
                    layout.prop(node, 'float_val', text='Value')
                elif node.data_type == 'INT':
                    layout.prop(node, 'int_val', text='Value')
                elif node.data_type == 'BOOL':
                    layout.prop(node, 'bool_val', text='Value')
                elif node.data_type == 'VECTOR':
                    layout.prop(node, 'vector_val', text='Value')
                elif node.data_type == 'STRING':
                    layout.prop(node, 'string_val', text='Value')
                layout.prop(node, 'expose_output')


def register():
    bpy.utils.register_class(SCENE_GRAPH_PT_node_properties)


def unregister():
    bpy.utils.unregister_class(SCENE_GRAPH_PT_node_properties)
