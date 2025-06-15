import bpy
from .base import BaseNode, SceneSocket

class OutputsStubNode(BaseNode):
    bl_idname = "OutputsStubNodeType"
    bl_label = "Render Outputs"

    filepath: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    file_format: bpy.props.EnumProperty(
        items=[('OPEN_EXR','OpenEXR',''),('PNG','PNG','')],
        name="Format"
    )

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.outputs.new('SceneSocketType', "Scene")