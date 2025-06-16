import bpy
from .base import BaseNode, build_props_and_sockets


class AlembicImportNode(BaseNode):
    bl_idname = "AlembicImportNodeType"
    bl_label = "Alembic Import"

    def init(self, context):
        self.add_enabled_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets


build_props_and_sockets(
    AlembicImportNode,
    [
        (
            "file_path",
            "string",
            {"name": "File Path", "subtype": "FILE_PATH"},
        ),
        ("scale", "float", {"name": "Scale", "default": 1.0}),
        ("set_frame_range", "bool", {"name": "Set Frame Range", "default": True}),
        ("validate_meshes", "bool", {"name": "Validate Meshes", "default": False}),
        (
            "always_add_cache_reader",
            "bool",
            {"name": "Add Cache Reader", "default": False},
        ),
        ("is_sequence", "bool", {"name": "Is Sequence", "default": False}),
        ("as_background_job", "bool", {"name": "Background Job", "default": False}),
    ],
)
