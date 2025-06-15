import bpy
from .base import (
    BaseNode,
    SceneSocket,
    StringSocket,
)

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
        fp = self.inputs.new('StringSocketType', "File Path")
        fp.value = self.filepath
        fmt = self.inputs.new('StringSocketType', "Format")
        fmt.value = self.file_format
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        layout.prop(self.inputs["File Path"], "value")
        layout.prop(self.inputs["Format"], "value")
