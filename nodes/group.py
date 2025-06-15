import bpy
from .base import BaseNode, SceneSocket

class GroupNode(BaseNode):
    bl_idname = "GroupNodeType"
    bl_label = "Group"

    num_inputs: bpy.props.IntProperty(
        name="Inputs",
        min=1,
        default=2,
        update=lambda self, ctx: self.update_sockets(),
    )

    def init(self, context):
        self.update_sockets()
        self.outputs.new('SceneSocketType', "Scene")

    def update_sockets(self):
        """Ensure the correct number of Scene inputs exist."""
        scene_inputs = [s for s in self.inputs if s.bl_idname == 'SceneSocketType']
        # Add sockets if needed
        while len(scene_inputs) < self.num_inputs:
            idx = len(scene_inputs) + 1
            scene_inputs.append(self.inputs.new('SceneSocketType', f"Scene {idx}"))
        # Remove extra sockets
        while len(scene_inputs) > self.num_inputs:
            sock = scene_inputs.pop()
            self.inputs.remove(sock)
        # Rename sockets to keep them ordered
        for idx, sock in enumerate(scene_inputs, 1):
            sock.name = f"Scene {idx}"

    def draw_buttons(self, context, layout):
        layout.prop(self, "num_inputs")
