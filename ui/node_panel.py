import bpy


def draw_node_properties(layout, node):
    """Draw UI elements for node properties and socket visibility."""
    for attr, label, _socket, typ in getattr(node.__class__, '_prop_defs', []):
        if hasattr(node, "is_property_visible") and not node.is_property_visible(attr):
            continue
        prop_name = f"use_{attr}"
        if not hasattr(node, prop_name):
            continue

        row = layout.row(align=True)
        row.prop(node, prop_name, text=label, toggle=True)

        if getattr(node, prop_name):
            sock = node.inputs.get(label)
            if sock is not None and not sock.is_linked:
                if typ == "enum":
                    row.prop(node, attr, text="")
                    if getattr(node, attr) != sock.value:
                        sock.value = getattr(node, attr)
                else:
                    row.prop(sock, "value", text="")

class SCENE_NODES_PT_node_props(bpy.types.Panel):
    bl_idname = "SCENE_NODES_PT_node_props"
    bl_label = "Node Properties"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Node'

    @classmethod
    def poll(cls, context):
        node = getattr(context, "active_node", None)
        if node is None:
            # In the Properties editor the active node is stored in `context.node`
            node = getattr(context, "node", None)
        return node is not None and hasattr(node.__class__, "_prop_defs")

    def draw(self, context):
        node = getattr(context, "active_node", None)
        if node is None:
            node = getattr(context, "node", None)
        layout = self.layout
        draw_node_properties(layout, node)


class SCENE_NODES_PT_socket_visibility(bpy.types.Panel):
    bl_idname = "SCENE_NODES_PT_socket_visibility"
    bl_label = "Socket Visibility"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Scene Nodes'

    @classmethod
    def poll(cls, context):
        node = getattr(context, "active_node", None)
        if node is None:
            node = getattr(context, "node", None)
        return node is not None and hasattr(node.__class__, "_prop_defs")

    def draw(self, context):
        node = getattr(context, "active_node", None)
        if node is None:
            node = getattr(context, "node", None)
        layout = self.layout
        draw_node_properties(layout, node)


class SCENE_NODES_PT_operators(bpy.types.Panel):
    """Panel with quick access to Scene Node operators."""
    bl_idname = "SCENE_NODES_PT_operators"
    bl_label = "Scene Node Operators"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Scene Nodes'

    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'SceneNodeTreeType'

    def draw(self, context):
        layout = self.layout
        layout.operator("scene_nodes.sync_to_scene")
        layout.operator("scene_nodes.render_pass_wedge")


class SCENE_NODES_PT_node_props_properties(SCENE_NODES_PT_node_props):
    bl_idname = "SCENE_NODES_PT_node_props_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'

def register():
    bpy.utils.register_class(SCENE_NODES_PT_node_props)
    bpy.utils.register_class(SCENE_NODES_PT_node_props_properties)
    bpy.utils.register_class(SCENE_NODES_PT_socket_visibility)
    bpy.utils.register_class(SCENE_NODES_PT_operators)


def unregister():
    bpy.utils.unregister_class(SCENE_NODES_PT_socket_visibility)
    bpy.utils.unregister_class(SCENE_NODES_PT_operators)
    bpy.utils.unregister_class(SCENE_NODES_PT_node_props_properties)
    bpy.utils.unregister_class(SCENE_NODES_PT_node_props)
