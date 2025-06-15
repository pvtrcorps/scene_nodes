import bpy
from .base import BaseNode, SceneSocket

class TransformNode(BaseNode):
    bl_idname = "TransformNodeType"
    bl_label = "Transform"

    translate: bpy.props.FloatVectorProperty(name="Translate", size=3)
    rotate: bpy.props.FloatVectorProperty(name="Rotate", size=3)
    scale: bpy.props.FloatVectorProperty(name="Scale", size=3, default=(1, 1, 1))

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.outputs.new('SceneSocketType', "Scene")