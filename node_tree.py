import bpy
from bpy.types import NodeTree

class SceneNodeTree(NodeTree):
    bl_idname = "SceneNodeTreeType"
    bl_label = "Scene Graph"
    bl_icon = 'NODETREE'