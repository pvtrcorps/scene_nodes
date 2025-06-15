import bpy
from .base import BaseNode, SceneSocket

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
        self.outputs.new('SceneSocketType', "Scene")