import bpy
from .base import BaseNode, build_props_and_sockets

class BlendInputNode(BaseNode):
    bl_idname = "BlendInputNodeType"
    bl_label = "Blend Input"

    def init(self, context):
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    BlendInputNode,
    [
        (
            "file_path",
            "string",
            {"name": "File Path", "subtype": "FILE_PATH"},
        ),
        (
            "collection_path",
            "string",
            {"name": "Collection Path"},
        ),
        (
            "load_mode",
            "enum",
            {
                "name": "Load Mode",
                "items": [
                    ("APPEND", "Append", "Append the collection"),
                    ("INSTANCE", "Instance", "Append collection and create instance object"),
                    ("LINK", "Link", "Link the collection"),
                    (
                        "OVERRIDE",
                        "Link Override",
                        "Link the collection and create a library override",
                    ),
                ],
                "default": "APPEND",
            },
        ),
        ("filter_expr", "string", {"name": "Filter"}),
    ],
)
