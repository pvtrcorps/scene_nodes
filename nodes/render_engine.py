import bpy
from .base import BaseNode, build_props_and_sockets


class RenderEngineNode(BaseNode):
    bl_idname = "RenderEngineNodeType"
    bl_label = "Render Engine"

    engine: bpy.props.EnumProperty(
        name="Engine",
        items=[('BLENDER_EEVEE', 'Eevee', ''), ('CYCLES', 'Cycles', '')],
        default='BLENDER_EEVEE',
        update=lambda self, ctx: self.update_engine(ctx),
    )

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")
        self.update_engine(context)

    def update_engine(self, context):
        cycle_attrs = {"feature_set", "device", "open_shading_language"}
        for attr in cycle_attrs:
            if self.engine == 'CYCLES' and getattr(self, f"use_{attr}", False):
                self.add_property_socket(attr)
            else:
                self.remove_property_socket(attr)

    def is_property_visible(self, attr):
        if attr in {"feature_set", "device", "open_shading_language"}:
            return self.engine == 'CYCLES'
        return True

    def draw_buttons(self, context, layout):
        layout.prop(self, "engine")


build_props_and_sockets(
    RenderEngineNode,
    [
        (
            "feature_set",
            "enum",
            {
                "name": "Feature Set",
                "items": [("SUPPORTED", "Supported", ""), ("EXPERIMENTAL", "Experimental", "")],
                "default": "SUPPORTED",
            },
        ),
        (
            "device",
            "enum",
            {
                "name": "Device",
                "items": [("CPU", "CPU", ""), ("GPU", "GPU", "")],
                "default": "CPU",
            },
        ),
        ("open_shading_language", "bool", {"name": "Open Shading Language"}),
    ],
)
