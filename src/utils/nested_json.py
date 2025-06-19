def safe_get(nested_obj: list | dict, path: list[int | str], default=None) -> str:
    """
    Safely get a value from nested lists/dicts.
    """

    try:
        for key in path:
            if isinstance(nested_obj, list) and isinstance(key, int):
                nested_obj = nested_obj[key]
            elif isinstance(nested_obj, dict):
                nested_obj = nested_obj[key]
            else:
                return default
        return nested_obj
    except (TypeError, IndexError, KeyError):
        return default