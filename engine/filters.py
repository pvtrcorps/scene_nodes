import fnmatch
def object_path(obj):
    """Return a collection/object path string for *obj*."""
    if not obj:
        return ""
    parts = []
    coll = obj.users_collection[0] if obj.users_collection else None
    while coll:
        parts.append(coll.name)
        coll = coll.parent
    parts.reverse()
    parts.append(obj.name)
    return "/".join(parts)


def matches(obj, pattern):
    """Return True if *obj* matches *pattern*."""
    if not pattern:
        return True
    path = object_path(obj)
    return fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(obj.name, pattern)


def filter_objects(objects, pattern):
    """Yield objects from *objects* matching *pattern*."""
    for obj in objects:
        if matches(obj, pattern):
            yield obj


def _collection_path(coll):
    """Return the hierarchical path for *coll* using parent names."""
    parts = []
    current = coll
    while current is not None:
        parts.append(current.name)
        current = getattr(current, "parent", None)
    parts.reverse()
    return "/".join(parts)


def filter_collections(collections, pattern):
    """Yield collections from *collections* whose name or path matches *pattern*."""
    for coll in collections:
        if not pattern:
            yield coll
            continue
        path = _collection_path(coll)
        if fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(coll.name, pattern):
            yield coll

