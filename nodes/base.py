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
    categories = []
    for desc in descriptors:
        if len(desc) == 3:
            attr, typ, kwargs = desc
            category = None
        elif len(desc) == 4:
            attr, typ, kwargs, category = desc
            if category and category not in categories:
                categories.append(category)
        else:
            raise ValueError("Invalid property descriptor")

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

    cls._categories = categories
    cls._category_prop_map = {}
    for cat in categories:
        prop_name = f"panel_show_{_sanitize(cat)}"
        setattr(cls, prop_name, bpy.props.BoolProperty(name=cat, default=True))
        cls._category_prop_map[cat] = prop_name

    return cls


class BaseNode(Node):
    bl_label = "Base Scene Node"
    bl_width_default = 200

    def init(self, context):
        """Override in subclasses to create mandatory sockets."""
        pass

    def add_property_sockets(self):
        """Ensure sockets for exposed properties exist."""
        self.update_sockets()

    def update_sockets(self, _context=None):
        """Create or remove sockets based on expose toggles."""
        cls = self.__class__
        for attr, label, socket_id, _cat in getattr(cls, '_prop_defs', []):
            expose_prop = cls._expose_prop_map.get(attr)
            if not expose_prop:
                continue
            exposed = getattr(self, expose_prop)
            sock = self.inputs.get(label)
            if exposed:
                if sock is None:
                    sock = self.inputs.new(socket_id, label)
                    try:
                        sock.value = getattr(self, attr)
                    except Exception:
                        pass
            else:
                if sock is not None:
                    self.inputs.remove(sock)

