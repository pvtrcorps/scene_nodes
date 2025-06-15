import bpy
from .base import BaseNode, build_props_and_sockets

class OutputsStubNode(BaseNode):
    bl_idname = "OutputsStubNodeType"
    bl_label = "Render Outputs"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_property_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    OutputsStubNode,
    [
        (
            "filepath",
            "string",
            {"name": "File Path", "subtype": "FILE_PATH"},
        ),
        (
            "file_format",
            "enum",
            {
                "items": [
                    ("OPEN_EXR", "OpenEXR", ""),
                    ("PNG", "PNG", ""),
                ],
                "name": "Format",
            },
        ),
    ],
)
