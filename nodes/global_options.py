import bpy
from .base import (
    BaseNode,
    SceneSocket,
    IntSocket,
    StringSocket,
)

class GlobalOptionsNode(BaseNode):
    bl_idname = "GlobalOptionsNodeType"
    bl_label = "Global Options"

    res_x: bpy.props.IntProperty(name="Resolution X", default=1920)
    res_y: bpy.props.IntProperty(name="Resolution Y", default=1080)
    samples: bpy.props.IntProperty(name="Samples", default=128)
    camera_path: bpy.props.StringProperty(name="Camera Path")

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        rx = self.inputs.new('IntSocketType', "Resolution X")
        rx.value = self.res_x
        ry = self.inputs.new('IntSocketType', "Resolution Y")
        ry.value = self.res_y
        sp = self.inputs.new('IntSocketType', "Samples")
        sp.value = self.samples
        cp = self.inputs.new('StringSocketType', "Camera Path")
        cp.value = self.camera_path
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets
