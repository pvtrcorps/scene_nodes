import bpy
from .base import (
    BaseNode,
    SceneSocket,
    StringSocket,
    BoolSocket,
)

class SceneInstanceNode(BaseNode):
    bl_idname = "SceneInstanceNodeType"
    bl_label = "Scene Instance"

    file_path: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    collection_path: bpy.props.StringProperty(name="Collection Path")
    as_override: bpy.props.BoolProperty(name="As Override", default=False)

    def init(self, context):
        fp = self.inputs.new('StringSocketType', "File Path")
        fp.value = self.file_path
        cp = self.inputs.new('StringSocketType', "Collection Path")
        cp.value = self.collection_path
        ov = self.inputs.new('BoolSocketType', "As Override")
        ov.value = self.as_override
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        layout.prop(self.inputs["File Path"], "value")
        layout.prop(self.inputs["Collection Path"], "value")
        layout.prop(self.inputs["As Override"], "value")
