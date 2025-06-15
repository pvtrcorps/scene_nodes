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
    # Get or create the ``__annotations__`` dictionary. ``cls.__dict__`` is
    # a read-only ``mappingproxy`` so ``setdefault`` cannot be used directly.
    annotations = getattr(cls, "__annotations__", None)
    if annotations is None:
        annotations = {}
        setattr(cls, "__annotations__", annotations)
    for attr, typ, kwargs in descriptors:
        prop_fn, socket_id = PROPERTY_SOCKET_MAP[typ]
        prop = prop_fn(**kwargs)
        setattr(cls, attr, prop)
        annotations[attr] = prop
        label = kwargs.get("name", attr)
        cls._prop_defs.append((attr, label, socket_id))

        # Boolean property controlling the socket visibility
        bool_name = f"use_{attr}"
        bool_prop = bpy.props.BoolProperty(
            name=f"Use {label}",
            default=True,
            update=lambda self, ctx, a=attr: self.update_socket_visibility(a),
        )
        setattr(cls, bool_name, bool_prop)
        annotations[bool_name] = bool_prop
    return cls


class BaseNode(Node):
    bl_label = "Base Scene Node"
    bl_width_default = 200

    def init(self, context):
        pass  # Definir sockets en cada nodo concreto

    def add_property_sockets(self):
        """Instantiate sockets for all defined properties."""
        for attr, _label, _socket in getattr(self.__class__, "_prop_defs", []):
            self.add_property_socket(attr)

    # ------------------------------------------------------------------
    # Socket management helpers
    # ------------------------------------------------------------------
    def _find_prop_def(self, attr):
        for a, label, socket in getattr(self.__class__, "_prop_defs", []):
            if a == attr:
                return label, socket
        return None, None

    def add_property_socket(self, attr):
        """Add the socket corresponding to *attr* if it doesn't exist."""
        label, socket = self._find_prop_def(attr)
        if label is None:
            return
        if self.inputs.get(label) is not None:
            return
        sock = self.inputs.new(socket, label)
        try:
            sock.value = getattr(self, attr)
        except Exception:
            pass

    def remove_property_socket(self, attr):
        """Remove the socket corresponding to *attr* if present."""
        label, _socket = self._find_prop_def(attr)
        if label is None:
            return
        sock = self.inputs.get(label)
        if sock is not None:
            self.inputs.remove(sock)

    def update_socket_visibility(self, attr):
        """Show or hide the socket for *attr* based on its use flag."""
        if getattr(self, f"use_{attr}", False):
            self.add_property_socket(attr)
        else:
            self.remove_property_socket(attr)

    def add_enabled_sockets(self):
        """Instantiate sockets only for properties with their use flag enabled."""
        for attr, _label, _socket in getattr(self.__class__, "_prop_defs", []):
            if getattr(self, f"use_{attr}", False):
                self.add_property_socket(attr)
