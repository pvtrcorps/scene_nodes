import bpy
from .base import build_props_and_sockets

RNASocketMap = {
    'BOOLEAN': 'BoolSocketType',
    'INT': 'IntSocketType',
    'FLOAT': 'FloatSocketType',
    'FLOAT_VECTOR': 'VectorSocketType',
    'STRING': 'StringSocketType',
    'ENUM': 'StringSocketType',
}

RnaTypeMap = {
    'BOOLEAN': 'bool',
    'INT': 'int',
    'FLOAT': 'float',
    'FLOAT_VECTOR': 'vector',
    'STRING': 'string',
    'ENUM': 'enum',
}


def descriptors_from_rna(rna_struct, exclude=None):
    """Build descriptors from a RNA struct."""
    if exclude is None:
        exclude = set()
    descs = []
    for prop in rna_struct.bl_rna.properties:
        if prop.identifier in {'rna_type'} or prop.identifier in exclude:
            continue
        if getattr(prop, 'is_hidden', False) or getattr(prop, 'is_readonly', False):
            continue
        typ = RnaTypeMap.get(prop.type)
        socket = RNASocketMap.get(prop.type)
        if typ is None or socket is None:
            continue
        kwargs = {'name': prop.name}
        if prop.type == 'ENUM':
            items = []
            for item in prop.enum_items:
                items.append((item.identifier, item.name, item.description))
            kwargs['items'] = items
        if prop.type in {'FLOAT_VECTOR'}:
            kwargs['size'] = prop.array_length
        descs.append((prop.identifier, typ, kwargs))
    return descs


def build_node_from_rna(cls, rna_struct, exclude=None):
    descs = descriptors_from_rna(rna_struct, exclude=exclude)
    build_props_and_sockets(cls, descs)
    return cls
