def check_object_name(obj, allowed_suffixes=("_geo", "_jnt", "_grp")):
    """
    Check if the object's name ends with one of the allowed suffixes.
    Allowed suffixes default to ("_geo", "_jnt", "_grp").
    """
    # allowed_suffixes can be a list or a tuple, ensure compatibility
    if not any(obj.name.endswith(suffix) for suffix in allowed_suffixes):
        return False, f"Object '{obj.name}' does not end with {allowed_suffixes}."
    return True, f"Object '{obj.name}' naming OK (ends with {allowed_suffixes})."