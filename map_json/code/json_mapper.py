from jsonify import jsonify
from map_value import map_value, Types

def map(data: dict | str, key, to_type=None, split_by: str = ".", default=None, return_default:bool=True):

    data = jsonify(data=data)
    value_dict = data.get(keystr=key, split_by=split_by, default=default, return_default=return_default)
    name = list(value_dict.keys())[0]
    value = list(value_dict.values())[0]
    if to_type is not None:
        if return_default:
            value = map_value(value=value, to_type=to_type, name=name, default=default)
        else:
            value = map_value(value=value, to_type=to_type, name=name)
    return {name: value}
