import datetime

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Types:
    STRING = "STRING"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BINARY = "BINARY"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"


def log_info(e: str):
    # return print(e)
    return logger.info

def _conversion_exception(value, name):
    return Exception(f"Failed to convert value {value} of type {type(value)} to Types.{name}")

def _convert_value_to_date_else_none(value):
    try:
        return datetime.datetime.strptime(value, "%m/%d/%Y")
    except:
        raise _conversion_exception(value=value, name=Types.DATE)
        
def _convert_value_to_datetime_else_none(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    except:
        raise _conversion_exception(value=value, name=Types.DATETIME)
    
def _convert_bool_to_binary_else_none(value):
    if not isinstance(value, bool):
        raise Exception(f"{value} is not a boolean. Failed to convert value to boolean.")
    if value is True:
        return 1
    elif value is False:
        return 0

def _convert_value_to_boolean_else_none(value):
    trues = [True, "true", "yes", 1, "Y"]
    falses = [False, "false", "no", 0, "N"]
    if value in trues:
        return True
    if value in falses:
        return False
    if value not in trues + falses:
        raise Exception(f"{value} does not belong to true values: {trues} or false values: {falses}")
    
def _convert_value_to_float_else_none(value):
    try:
        return float(value)
    except:
        raise _conversion_exception(value=value, name=Types.DECIMAL)
    
def _convert_value_to_int_else_none(value):
    try:
        return int(value)
    except:
        raise _conversion_exception(value=value, name=Types.INTEGER)
    
def _convert_value_to_str_else_none(value):
    try:
        return str(value)
    except:
        raise _conversion_exception(value=value, name=Types.STRING)


def map_value(value=None, to_type: str = Types.STRING, name: str = "Value:", default=None):

    conversion_mapper = {
        Types.STRING: _convert_value_to_str_else_none,
        Types.DATE: _convert_value_to_date_else_none,
        Types.DATETIME: _convert_value_to_datetime_else_none,
        Types.BINARY: _convert_bool_to_binary_else_none,
        Types.BOOLEAN: _convert_value_to_boolean_else_none,
        Types.INTEGER: _convert_value_to_int_else_none,
        Types.DECIMAL: _convert_value_to_float_else_none,
    }

    if to_type not in conversion_mapper:
        error = f"{to_type} is not available in available types: {conversion_mapper.keys()}"
        raise Exception(error)
    
    convert = conversion_mapper.get(to_type, None)
    
    if value is None:
        log_info(f"{name} value {value} is {None}")
        if default is None:
            return default
        if default is not None:
            try:
                return convert(value=default)
            except Exception as e:
                log_info(f"Failed to convert default value {default} for {name} to {to_type}. error: {e}")
            return None
    
    if value is not None:
        try:
            return convert(value=value)
        except Exception as e:
            log_info(f"Failed to convert {name}: {value} to {to_type}. Exception: {e}")
