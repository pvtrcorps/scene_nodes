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


class EnumSocket(NodeSocket):
    bl_idname = "EnumSocketType"
    bl_label = "Enum"

    value: bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        attr = getattr(self, "scene_nodes_attr", None)
        if attr and hasattr(node, attr):
            layout.prop(node, attr, text=text)
            try:
                self.value = getattr(node, attr)
            except Exception:
                pass
        else:
            layout.prop(self, "value", text=text)

    def draw_color(self, context, node):
        return (0.7, 0.7, 0.7, 1.0)

PROPERTY_SOCKET_MAP = {
    'float': (bpy.props.FloatProperty, 'FloatSocketType'),
    'int': (bpy.props.IntProperty, 'IntSocketType'),
    'bool': (bpy.props.BoolProperty, 'BoolSocketType'),
    'vector': (bpy.props.FloatVectorProperty, 'VectorSocketType'),
    'string': (bpy.props.StringProperty, 'StringSocketType'),
    'enum': (bpy.props.EnumProperty, 'EnumSocketType'),
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
        cls._prop_defs.append((attr, label, socket_id, typ))

        # Boolean property controlling the socket visibility
        bool_name = f"use_{attr}"
        def _make_update(name):
            def _update(self, ctx):
                self.update_socket_visibility(name)
            return _update

        bool_prop = bpy.props.BoolProperty(
            name=f"Use {label}",
            default=True,
            update=_make_update(attr),
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
        for attr, _label, _socket, _typ in getattr(self.__class__, "_prop_defs", []):
            self.add_property_socket(attr)

    # ------------------------------------------------------------------
    # Socket management helpers
    # ------------------------------------------------------------------
    def _find_prop_def(self, attr):
        for a, label, socket, typ in getattr(self.__class__, "_prop_defs", []):
            if a == attr:
                return label, socket, typ
        return None, None, None

    def add_property_socket(self, attr):
        """Add the socket corresponding to *attr* if it doesn't exist."""
        label, socket, _typ = self._find_prop_def(attr)
        if label is None:
            return
        if self.inputs.get(label) is not None:
            return
        sock = self.inputs.new(socket, label)
        sock.scene_nodes_attr = attr
        try:
            sock.value = getattr(self, attr)
        except Exception:
            pass

        # Reorder socket according to property definition order
        new_index = len(self.inputs) - 1
        order_map = {
            lbl: idx
            for idx, (_a, lbl, _s, _t) in enumerate(
                getattr(self.__class__, "_prop_defs", [])
            )
        }
        prop_pos = order_map.get(label, new_index)
        target_index = 0
        for i, s in enumerate(self.inputs):
            if s is sock:
                continue
            other_pos = order_map.get(s.name)
            if other_pos is None or other_pos < prop_pos:
                target_index = i + 1
            else:
                break
        if target_index != new_index:
            self.inputs.move(new_index, target_index)

    def remove_property_socket(self, attr):
        """Remove the socket corresponding to *attr* if present."""
        label, _socket, _typ = self._find_prop_def(attr)
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
        for attr, _label, _socket, _typ in getattr(self.__class__, "_prop_defs", []):
            if getattr(self, f"use_{attr}", False):
                self.add_property_socket(attr)

    def is_property_visible(self, _attr):
        """Override in subclasses to hide properties from the panels."""
        return True
