import bpy
from .base import BaseNode, SceneSocket

class GlobalOptionsNode(BaseNode):
    bl_idname = "GlobalOptionsNodeType"
    bl_label = "Global Options"

    res_x: bpy.props.IntProperty(name="Resolution X", default=1920)
    res_y: bpy.props.IntProperty(name="Resolution Y", default=1080)
    samples: bpy.props.IntProperty(name="Samples", default=128)
    camera_path: bpy.props.StringProperty(name="Camera Path")

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.outputs.new('SceneSocketType', "Scene")