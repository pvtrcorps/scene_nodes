import bpy
from .base import (
    BaseNode,
    SceneSocket,
    VectorSocket,
)

class TransformNode(BaseNode):
    bl_idname = "TransformNodeType"
    bl_label = "Transform"

    translate: bpy.props.FloatVectorProperty(name="Translate", size=3)
    rotate: bpy.props.FloatVectorProperty(name="Rotate", size=3)
    scale: bpy.props.FloatVectorProperty(name="Scale", size=3, default=(1, 1, 1))

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        t = self.inputs.new('VectorSocketType', "Translate")
        t.value = self.translate
        r = self.inputs.new('VectorSocketType', "Rotate")
        r.value = self.rotate
        s = self.inputs.new('VectorSocketType', "Scale")
        s.value = self.scale
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets
