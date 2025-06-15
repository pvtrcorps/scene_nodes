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
            categories = getattr(cls, '_categories', [])
            if categories:
                for cat in categories:
                    prop_name = cls._category_prop_map.get(cat)
                    expanded = getattr(node, prop_name)
                    box = layout.box()
                    row = box.row()
                    row.prop(node, prop_name, icon='TRIA_DOWN' if expanded else 'TRIA_RIGHT', emboss=False, icon_only=True)
                    row.label(text=cat)
                    if expanded:
                        for attr, label, _socket, category in cls._prop_defs:
                            if category == cat:
                                expose = cls._expose_prop_map.get(attr)
                                if expose:
                                    box.prop(node, expose, text=label)
            for attr, label, _socket, category in getattr(cls, '_prop_defs', []):
                if category is None:
                    expose = cls._expose_prop_map.get(attr)
                    if expose:
                        layout.prop(node, expose, text=label)
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
