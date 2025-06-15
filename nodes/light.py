import bpy
from .base import BaseNode, build_props_and_sockets

class LightNode(BaseNode):
    bl_idname = "LightNodeType"
    bl_label = "Light"

    def init(self, context):
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    LightNode,
    [
        (
            "light_type",
            "enum",
            {
                "items": [
                    ("POINT", "Point", ""),
                    ("SUN", "Sun", ""),
                    ("SPOT", "Spot", ""),
                    ("AREA", "Area", ""),
                ],
                "name": "Type",
            },
        ),
        ("energy", "float", {"name": "Energy", "default": 10.0}),
        (
            "color",
            "vector",
            {"name": "Color", "subtype": "COLOR", "default": (1, 1, 1)},
        ),
    ],
)
