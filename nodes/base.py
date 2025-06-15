import bpy
from bpy.types import Node, NodeSocket

class SceneSocket(NodeSocket):
    bl_idname = "SceneSocketType"
    bl_label = "Scene"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.8, 0.8, 0.2, 1.0)


class FloatSocket(NodeSocket):
    bl_idname = "FloatSocketType"
    bl_label = "Float"

    value: bpy.props.FloatProperty()

    def draw(self, context, layout, node, text):
        layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)


class IntSocket(NodeSocket):
    bl_idname = "IntSocketType"
    bl_label = "Int"

    value: bpy.props.IntProperty()

    def draw(self, context, layout, node, text):
        layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)


class BoolSocket(NodeSocket):
    bl_idname = "BoolSocketType"
    bl_label = "Bool"

    value: bpy.props.BoolProperty()

    def draw(self, context, layout, node, text):
        layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)


class VectorSocket(NodeSocket):
    bl_idname = "VectorSocketType"
    bl_label = "Vector"

    value: bpy.props.FloatVectorProperty(size=3)

    def draw(self, context, layout, node, text):
        layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)


class StringSocket(NodeSocket):
    bl_idname = "StringSocketType"
    bl_label = "String"

    value: bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)

PROPERTY_SOCKET_MAP = {
    'float': (bpy.props.FloatProperty, 'FloatSocketType'),
    'int': (bpy.props.IntProperty, 'IntSocketType'),
    'bool': (bpy.props.BoolProperty, 'BoolSocketType'),
    'vector': (bpy.props.FloatVectorProperty, 'VectorSocketType'),
    'string': (bpy.props.StringProperty, 'StringSocketType'),
    'enum': (bpy.props.EnumProperty, 'StringSocketType'),
}


def build_props_and_sockets(cls, descriptors):
    """Create node properties and remember socket information.

    Parameters
    ----------
    cls : type
        Node class where the properties will be added.
    descriptors : iterable
        Each item must be ``(attr_name, type_key, kwargs)`` where ``type_key``
        is a key of :data:`PROPERTY_SOCKET_MAP` and ``kwargs`` are passed
        directly to ``bpy.props``.
    """
    cls._prop_defs = []
    if not hasattr(cls, "__annotations__"):
        cls.__annotations__ = {}
    for attr, typ, kwargs in descriptors:
        prop_fn, socket_id = PROPERTY_SOCKET_MAP[typ]
        prop = prop_fn(**kwargs)
        setattr(cls, attr, prop)
        cls.__annotations__[attr] = prop
        label = kwargs.get('name', attr)
        cls._prop_defs.append((attr, label, socket_id))
        bool_prop = bpy.props.BoolProperty(
            name=f"Use {label}",
            default=True,
            update=lambda self, ctx, a=attr, sid=socket_id, l=label: self.toggle_property_socket(a, sid, l),
        )
        setattr(cls, f"use_{attr}", bool_prop)
        cls.__annotations__[f"use_{attr}"] = bool_prop
    return cls


class BaseNode(Node):
    bl_label = "Base Scene Node"
    bl_width_default = 200

    def init(self, context):
        self._property_sockets = {}

    def add_property_sockets(self):
        """Instantiate sockets for the properties defined via
        :func:`build_props_and_sockets`."""
        for attr, label, socket in getattr(self.__class__, '_prop_defs', []):
            if getattr(self, f"use_{attr}", True):
                sock = self.inputs.new(socket, label)
                self._property_sockets[attr] = sock
                try:
                    sock.value = getattr(self, attr)
                except Exception:
                    pass

    def toggle_property_socket(self, attr, sid, label):
        """Add or remove a socket based on ``use_<attr>``."""
        use = getattr(self, f"use_{attr}")
        sock = self._property_sockets.get(attr)
        if use and sock is None:
            sock = self.inputs.new(sid, label)
            self._property_sockets[attr] = sock
            try:
                sock.value = getattr(self, attr)
            except Exception:
                pass
        elif not use and sock is not None:
            self.inputs.remove(sock)
            del self._property_sockets[attr]
