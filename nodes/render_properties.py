import bpy
from .base import BaseNode, build_props_and_sockets


class RenderPropertiesNode(BaseNode):
    bl_idname = "RenderPropertiesNodeType"
    bl_label = "Render Properties"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    RenderPropertiesNode,
    [
        (
            "engine",
            "enum",
            {
                "name": "Engine",
                "items": [
                    ("BLENDER_EEVEE", "Eevee", ""),
                    ("CYCLES", "Cycles", ""),
                    ("BLENDER_WORKBENCH", "Workbench", ""),
                ],
                "default": "BLENDER_EEVEE",
            },
        ),
        ("samples", "int", {"name": "Samples", "default": 128}),
    ],
)
