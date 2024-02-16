import os
import json
from typing import Union

class Types:
    LIST = "LIST"
    DICT = "DICT"
    TUPLE = "TUPLE"


class jsonify:
    def __init__(self, data: dict | str) -> None:
        self.data = self.set_data(data=data)

    def set_data(self, data):
        if isinstance(data, dict):
            return data
        if isinstance(data, list):
            return data
        if isinstance(data, str):
            if not os.path.exists(data):
                raise Exception(f"Path {data} does not exist in scope.")
            try:
                with open(data, 'r') as f:
                    return json.load(f)
            except Exception as e:
                raise e
        return None
    
    @staticmethod
    def identify(string):
        if "[" in string and "]" in string:
            return Types.LIST
        if "{" in string and "}" in string:
            return Types.DICT
        if "(" in string and ")" in string:
            return Types.TUPLE

    @staticmethod
    def _perform_list_operation(data: list, key: str):
        try:
            index = int(key.strip("[]"))
            return data[index]
        except Exception as e:
            raise e

    @staticmethod
    def _perform_dict_operation(data: dict, key: str):
        try:
            key = key.strip("{}")
            if not key in data:
                raise Exception(f"{key} not in {data}. Failed dict operation.")
            return data[key]
        except Exception as e:
            raise e
    
    @staticmethod
    def _perform_tuple_operation(data: tuple, key: str):
        try:
            index = int(key.strip("()"))
            return data[index]
        except Exception as e:
            raise e

    @staticmethod
    def _validate_data_type(data, identity):
        identity_types = {
            Types.LIST: list,
            Types.DICT: dict,
            Types.TUPLE: tuple
        }

        if identity not in identity_types:
            raise Exception(f"Unable to validate data with given identity {identity}")
        
        if isinstance(data, identity_types.get(identity)):
            return True
        return False

    @staticmethod
    def _get_func(identity):
        funcs = {
            Types.LIST : jsonify._perform_list_operation,
            Types.DICT : jsonify._perform_dict_operation,
            Types.TUPLE: jsonify._perform_tuple_operation
        }

        if identity not in funcs:
            raise Exception(f"Identity '{identity}' does not exist.")
        
        return funcs.get(identity)
    
    @staticmethod
    def _extract_value(data, key):
        identity = jsonify.identify(string=key)

        if not jsonify._validate_data_type(data=data, identity=identity):
            raise Exception(f"Unable to validate data {data} with key '{key}'. Expected type {identity}, received {type(data)} as input.")

        try:
            extract = jsonify._get_func(identity=identity)
            value = extract(data=data, key=key)
            return value
        except Exception as e:
            raise e
                

    def get(self, keystr: str, split_by: str = ".", default=None, return_default:bool=False):
        if not isinstance(keystr, str) or not isinstance(split_by, str):
            raise Exception(f"'jsonify.get' only takes strings as args. Args passed keystr : {type(keystr)}, split_by: {type(split_by)}")
        
        iterative_keys = keystr.split(split_by)
        data = self.data.copy()
        for idx, key in enumerate(iterative_keys):
            print(f"METHOD jsonify.get : key: {key} ---- index: {idx+1}/{len(iterative_keys)}----- identity: {jsonify.identify(string=key)} --- data: {data}")
            try:
                value = jsonify._extract_value(data=data, key=key)
                if idx == len(iterative_keys) - 1:
                    return {key.strip("{[()]}"): value}
                data = value
            except Exception as e:
                if return_default:
                    return {"default": default}
                raise e
