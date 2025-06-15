import bpy
from bpy.types import Node, NodeSocket

class SceneSocket(NodeSocket):
    bl_idname = "SceneSocketType"
    bl_label = "Scene"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 0.2, 1.0)

class BaseNode(Node):
    bl_label = "Base Scene Node"
    bl_width_default = 200

    def init(self, context):
        pass  # Definir sockets en cada nodo concreto