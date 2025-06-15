import bpy
from .base import (
    BaseNode,
    FloatSocket,
    IntSocket,
    BoolSocket,
    VectorSocket,
    StringSocket,
)


class InputNode(BaseNode):
    bl_idname = "InputNodeType"
    bl_label = "Input"

    input_type: bpy.props.EnumProperty(
        items=[
            ('FLOAT', 'Float', ''),
            ('INT', 'Int', ''),
            ('VECTOR', 'Vector', ''),
            ('STRING', 'String', ''),
            ('BOOL', 'Bool', ''),
        ],
        name="Type",
        default='FLOAT',
        update=lambda self, context: self._update_socket()
    )

    float_value: bpy.props.FloatProperty(name="Float Value", default=0.0)
    int_value: bpy.props.IntProperty(name="Int Value", default=0)
    bool_value: bpy.props.BoolProperty(name="Bool Value", default=False)
    vector_value: bpy.props.FloatVectorProperty(name="Vector Value", size=3)
    string_value: bpy.props.StringProperty(name="String Value")

    def _socket_type(self):
        mapping = {
            'FLOAT': 'FloatSocketType',
            'INT': 'IntSocketType',
            'VECTOR': 'VectorSocketType',
            'STRING': 'StringSocketType',
            'BOOL': 'BoolSocketType',
        }
        return mapping.get(self.input_type, 'FloatSocketType')

    def _socket_value(self):
        return {
            'FLOAT': self.float_value,
            'INT': self.int_value,
            'VECTOR': self.vector_value,
            'STRING': self.string_value,
            'BOOL': self.bool_value,
        }.get(self.input_type, None)

    def _update_socket(self):
        if self.outputs:
            self.outputs.remove(self.outputs[0])
        sock = self.outputs.new(self._socket_type(), "Value")
        value = self._socket_value()
        if value is not None:
            sock.value = value

    def init(self, context):
        self.outputs.new(self._socket_type(), "Value")

    def draw_buttons(self, context, layout):
        layout.prop(self, "input_type")
        if self.input_type == 'FLOAT':
            layout.prop(self, "float_value", text="Value")
        elif self.input_type == 'INT':
            layout.prop(self, "int_value", text="Value")
        elif self.input_type == 'VECTOR':
            layout.prop(self, "vector_value", text="Value")
        elif self.input_type == 'STRING':
            layout.prop(self, "string_value", text="Value")
        elif self.input_type == 'BOOL':
            layout.prop(self, "bool_value", text="Value")
