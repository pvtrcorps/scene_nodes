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

