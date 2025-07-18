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

    data_type: bpy.props.EnumProperty(
        name="Type",
        items=[
            ('FLOAT', "Float", ""),
            ('INT', "Int", ""),
            ('BOOL', "Bool", ""),
            ('VECTOR', "Vector", ""),
            ('STRING', "String", ""),
        ],
        default='FLOAT',
        update=lambda self, context: self.update_socket(),
    )

    float_val: bpy.props.FloatProperty(update=lambda self, ctx: self.update_socket_value())
    int_val: bpy.props.IntProperty(update=lambda self, ctx: self.update_socket_value())
    bool_val: bpy.props.BoolProperty(update=lambda self, ctx: self.update_socket_value())
    vector_val: bpy.props.FloatVectorProperty(size=3, update=lambda self, ctx: self.update_socket_value())
    string_val: bpy.props.StringProperty(update=lambda self, ctx: self.update_socket_value())

    def init(self, context):
        self.update_socket()

    def update_socket(self):
        while self.outputs:
            self.outputs.remove(self.outputs[0])
        type_map = {
            'FLOAT': 'FloatSocketType',
            'INT': 'IntSocketType',
            'BOOL': 'BoolSocketType',
            'VECTOR': 'VectorSocketType',
            'STRING': 'StringSocketType',
        }
        stype = type_map.get(self.data_type, 'FloatSocketType')
        self.outputs.new(stype, "Value")
        self.update_socket_value()

    def update_socket_value(self):
        if not self.outputs:
            return
        sock = self.outputs[0]
        if self.data_type == 'FLOAT':
            sock.value = self.float_val
        elif self.data_type == 'INT':
            sock.value = self.int_val
        elif self.data_type == 'BOOL':
            sock.value = self.bool_val
        elif self.data_type == 'VECTOR':
            sock.value = self.vector_val
        elif self.data_type == 'STRING':
            sock.value = self.string_val

    def draw_buttons(self, context, layout):
        layout.prop(self, "data_type")
        if self.data_type == 'FLOAT':
            layout.prop(self, "float_val", text="Value")
        elif self.data_type == 'INT':
            layout.prop(self, "int_val", text="Value")
        elif self.data_type == 'BOOL':
            layout.prop(self, "bool_val", text="Value")
        elif self.data_type == 'VECTOR':
            layout.prop(self, "vector_val", text="Value")
        elif self.data_type == 'STRING':
            layout.prop(self, "string_val", text="Value")
