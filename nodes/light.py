import bpy
from .base import (
    BaseNode,
    SceneSocket,
    FloatSocket,
    StringSocket,
    VectorSocket,
)

class LightNode(BaseNode):
    bl_idname = "LightNodeType"
    bl_label = "Light"

    light_type: bpy.props.EnumProperty(
        items=[('POINT','Point',''),('SUN','Sun',''),('SPOT','Spot',''),('AREA','Area','')],
        name="Type"
    )
    energy: bpy.props.FloatProperty(name="Energy", default=10.0)
    color: bpy.props.FloatVectorProperty(name="Color", subtype='COLOR', default=(1,1,1))

    def init(self, context):
        t = self.inputs.new('StringSocketType', "Type")
        t.value = self.light_type
        e = self.inputs.new('FloatSocketType', "Energy")
        e.value = self.energy
        c = self.inputs.new('VectorSocketType', "Color")
        c.value = self.color
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        pass  # Inputs already expose editable values next to their sockets
