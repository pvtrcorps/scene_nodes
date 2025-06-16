import bpy
from .base import BaseNode, build_props_and_sockets


class RenderPropertiesNode(BaseNode):
    bl_idname = "RenderPropertiesNodeType"
    bl_label = "Render Properties"

    def update_engine(self, _context=None):
        sock = self.inputs.get("Engine")
        if sock is not None:
            sock.value = self.engine
        if self.engine == "BLENDER_EEVEE":
            self.remove_property_socket("max_bounces")
            if getattr(self, "use_motion_blur", False):
                self.add_property_socket("motion_blur")
        elif self.engine == "CYCLES":
            self.remove_property_socket("motion_blur")
            if getattr(self, "use_max_bounces", False):
                self.add_property_socket("max_bounces")
        else:
            self.remove_property_socket("motion_blur")
            self.remove_property_socket("max_bounces")

    def init(self, context):
        self.inputs.new('SceneSocketType', "Scene")
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")
        self.update_engine()

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets

    def is_property_visible(self, attr):
        if attr == "motion_blur":
            return self.engine == "BLENDER_EEVEE"
        if attr == "max_bounces":
            return self.engine == "CYCLES"
        return True


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
                "update": lambda self, ctx: self.update_engine(),
            },
        ),
        ("samples", "int", {"name": "Samples", "default": 64}),
        ("motion_blur", "bool", {"name": "Motion Blur"}),
        ("max_bounces", "int", {"name": "Max Bounces", "default": 8}),
    ],
)
