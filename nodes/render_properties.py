import bpy
from .base import BaseNode, PROPERTY_SOCKET_MAP
from .property_utils import descriptors_from_rna


class RenderSettingsNode(BaseNode):
    bl_idname = "RenderSettingsNodeType"
    bl_label = "Render Settings"

    engine_items = [
        ('BLENDER_EEVEE', 'Eevee', ''),
        ('CYCLES', 'Cycles', ''),
    ]

    engine_path_map = {
        'BLENDER_EEVEE': ['eevee'],
        'CYCLES': ['cycles'],
    }

    engine: bpy.props.EnumProperty(
        name="Engine",
        items=engine_items,
        default='BLENDER_EEVEE',
        update=lambda self, ctx: self.update_engine(ctx),
    )

    _engine_prop_defs = []  # (attr_pref, rna_attr, label, socket_id, engine)

    def update_engine(self, context):
        for attr, _rna, label, _sid, eng in self.__class__._engine_prop_defs:
            sock = self._property_sockets.get(attr)
            if sock:
                sock.hide = eng != self.engine

    def init(self, context):
        self._property_sockets = {}
        self.inputs.new('SceneSocketType', "Scene")
        for attr, _rna, label, sid, eng in self.__class__._engine_prop_defs:
            sock = self.inputs.new(sid, label)
            self._property_sockets[attr] = sock
            sock.hide = eng != self.engine
            try:
                sock.value = getattr(self, attr)
            except Exception:
                pass
        self.outputs.new('SceneSocketType', "Scene")

    def draw_buttons(self, context, layout):
        layout.prop(self, "engine", text="Engine")


def _build_engine_props(cls, engine, rna_struct):
    descs = descriptors_from_rna(rna_struct)
    for identifier, typ, kwargs in descs:
        prop_fn, socket_id = PROPERTY_SOCKET_MAP[typ]
        attr = f"{engine.lower()}_{identifier}"
        setattr(cls, attr, prop_fn(**kwargs))
        label = kwargs.get('name', identifier)
        cls._engine_prop_defs.append((attr, identifier, label, socket_id, engine))
    return cls


def _resolve_settings_struct(prop_name, fallback):
    cls = getattr(bpy.types, fallback, None)
    if cls is None:
        prop = bpy.types.Scene.bl_rna.properties.get(prop_name)
        if prop is not None and hasattr(prop, "fixed_type"):
            ident = getattr(prop.fixed_type, "identifier", None)
            if ident:
                cls = getattr(bpy.types, ident, None)
    return cls


cycles_struct = _resolve_settings_struct("cycles", "CyclesRenderSettings")
if cycles_struct is not None:
    _build_engine_props(RenderSettingsNode, 'CYCLES', cycles_struct)

eevee_struct = _resolve_settings_struct("eevee", "EeveeRenderSettings")
if eevee_struct is not None:
    _build_engine_props(RenderSettingsNode, 'BLENDER_EEVEE', eevee_struct)

__all__ = ["RenderSettingsNode"]
