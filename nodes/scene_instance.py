import bpy
from .base import BaseNode, SceneSocket

class SceneInstanceNode(BaseNode):
    bl_idname = "SceneInstanceNodeType"
    bl_label = "Scene Instance"

    file_path: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    collection_path: bpy.props.StringProperty(name="Collection Path")
    as_override: bpy.props.BoolProperty(name="As Override", default=False)

    def init(self, context):
        self.outputs.new('SceneSocketType', "Scene")