import bpy
from .base import BaseNode, SceneSocket

class GroupNode(BaseNode):
    bl_idname = "GroupNodeType"
    bl_label = "Group"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene 1")
        self.inputs.new('SceneSocketType', "Scene 2")
        self.outputs.new('SceneSocketType', "Scene")