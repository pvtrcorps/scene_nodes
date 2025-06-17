import bpy
from .base import BaseNode, build_props_and_sockets


class EeveeAttributesNode(BaseNode):
    bl_idname = "EeveeAttributesNodeType"
    bl_label = "Eevee Attributes"

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    EeveeAttributesNode,
    [
        ("hide_render", "bool", {"name": "Hide Render"}),
        ("is_shadow_catcher", "bool", {"name": "Shadow Catcher"}),
        ("is_holdout", "bool", {"name": "Holdout"}),
        ("visible_camera", "bool", {"name": "Visible Camera", "default": True}),
        ("visible_diffuse", "bool", {"name": "Visible Diffuse", "default": True}),
        ("visible_glossy", "bool", {"name": "Visible Glossy", "default": True}),
        ("visible_transmission", "bool", {"name": "Visible Transmission", "default": True}),
        ("visible_volume_scatter", "bool", {"name": "Visible Volume", "default": True}),
        ("visible_shadow", "bool", {"name": "Visible Shadow", "default": True}),
        ("filter_expr", "string", {"name": "Filter"}),
    ],
)
