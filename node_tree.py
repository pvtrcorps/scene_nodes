import bpy
from bpy.types import NodeTree


class SceneNodeTree(NodeTree):
    """Custom node tree for building scene graphs in Blender.

    The ``SceneNodeTreeType`` identifier allows this tree to appear in the
    Node Editor. The methods below implement the typical hooks Blender expects
    for custom trees so the editor can properly handle creation, updates and
    deletion of this tree type.
    """

    bl_idname = "SceneNodeTreeType"
    bl_label = "Scene Graph"
    bl_icon = 'NODETREE'

    @classmethod
    def poll(cls, context):
        """Limit availability to node editors."""
        return context.area is not None and context.area.type == 'NODE_EDITOR'

    def update(self):
        """Called when the tree is changed."""
        pass

    def update_node(self, node):
        """Called when a node inside the tree changes."""
        self.update()

    def socket_value_update(self, context):
        """Called when a socket value is modified."""
        self.update()

    def free(self):
        """Called when the tree is removed from memory."""
        pass

    def copy(self, node_tree):
        """Called when the tree is duplicated."""
        pass

