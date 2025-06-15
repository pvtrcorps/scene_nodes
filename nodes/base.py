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


def _sanitize(name):
    """Return a valid identifier for ``name``."""
    import re
    return re.sub(r"[^0-9a-zA-Z_]", "_", name).lower()


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
    cls._expose_prop_map = {}
    for desc in descriptors:
        if len(desc) < 3:
            raise ValueError("Invalid property descriptor")
        attr, typ, kwargs = desc[:3]
        category = desc[3] if len(desc) > 3 else None

        prop_fn, socket_id = PROPERTY_SOCKET_MAP[typ]
        setattr(cls, attr, prop_fn(**kwargs))
        label = kwargs.get('name', attr)
        expose_prop = f"expose_{_sanitize(attr)}"
        setattr(
            cls,
            expose_prop,
            bpy.props.BoolProperty(
                name=f"Expose {label}",
                default=False,
                update=BaseNode.update_sockets,
            ),
        )
        cls._expose_prop_map[attr] = expose_prop
        cls._prop_defs.append((attr, label, socket_id, category))

    return cls


class BaseNode(Node):
    bl_label = "Base Scene Node"
    bl_width_default = 200

    def init(self, context):
        pass  # Definir sockets en cada nodo concreto

    def add_property_sockets(self):
        """Instantiate sockets for the properties defined via
        :func:`build_props_and_sockets`."""
        for info in getattr(self.__class__, '_prop_defs', []):
            attr, label, socket, *_ = info
            sock = self.inputs.new(socket, label)
            expose_prop = self.__class__._expose_prop_map.get(attr)
            if expose_prop:
                sock.hide = not getattr(self, expose_prop)
            try:
                sock.value = getattr(self, attr)
            except Exception:
                pass
        self.update_sockets()

    def update_sockets(self, _context=None):
        cls = self.__class__
        for attr, label, _socket, *_ in getattr(cls, '_prop_defs', []):
            expose_prop = cls._expose_prop_map.get(attr)
            if expose_prop:
                sock = self.inputs.get(label)
                if sock:
                    sock.hide = not getattr(self, expose_prop)

