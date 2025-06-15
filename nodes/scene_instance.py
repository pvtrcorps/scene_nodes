import bpy
from .base import (
    BaseNode,
    SceneSocket,
    StringSocket,
)

class SceneInstanceNode(BaseNode):
    bl_idname = "SceneInstanceNodeType"
    bl_label = "Scene Instance"

    file_path: bpy.props.StringProperty(name="File Path", subtype='FILE_PATH')
    collection_path: bpy.props.StringProperty(name="Collection Path")
    load_mode: bpy.props.EnumProperty(
        name="Load Mode",
        items=[
            ('APPEND', "Append", "Append the collection"),
            ('INSTANCE', "Instance", "Append collection and create instance object"),
            ('LINK', "Link", "Link the collection"),
            ('OVERRIDE', "Link Override", "Link the collection and create a library override"),
        ],
        default='APPEND'
    )

    def init(self, context):
        fp = self.inputs.new('StringSocketType', "File Path")
        fp.value = self.file_path
        cp = self.inputs.new('StringSocketType', "Collection Path")
        cp.value = self.collection_path
        lm = self.inputs.new('StringSocketType', "Load Mode")
        lm.value = self.load_mode
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets
