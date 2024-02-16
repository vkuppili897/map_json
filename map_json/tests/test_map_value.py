import os
import sys
import pytest
import datetime


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
code_dir_path = os.path.join(base_path, 'code')
sys.path.append(code_dir_path)

from map_value import map_value, Types


class TestMappingService:

    def test_map_value_to_str(self):
        values = [1, "1"]
        expect = "1"

        for val in values:
            result = map_value(value=val, to_type = Types.STRING)
            assert result == expect

    def test_map_value_to_int(self):
        values = [1, "1"]
        expect = 1

        for val in values:
            result = map_value(value=val, to_type = Types.INTEGER)
            assert result == expect

    def test_map_value_to_decimal(self):
        values = [1, "1", 1.0, "1.0"]
        expect = 1.0

        for val in values:
            result = map_value(value=val, to_type = Types.DECIMAL)
            assert result == expect

    def test_map_bool_to_binary(self):
        val = True
        expect = 1
        result = map_value(value=val, to_type = Types.BINARY)
        assert result == expect

        val = False
        expect = 0
        result = map_value(value=val, to_type = Types.BINARY)
        assert result == expect

    def test_map_to_boolean(self):
        trues = [1, "Y", "yes", "true", True]
        expect = True

        for val in trues:
            result = map_value(value=val, to_type = Types.BOOLEAN)
            assert result == expect

        falses = [0, "N", "no", "false", False]
        expect = False

        for val in falses:
            result = map_value(value=val, to_type = Types.BOOLEAN)
            assert result == expect

    
    def test_map_to_date(self):
        value = "01/19/2024"
        expect = datetime.datetime(year=2024, month=1, day=19)
        result = map_value(value=value, to_type = Types.DATE)
        assert result == expect

    def test_map_to_datetime(self):
        value = "2024-01-19T00:00:00"
        expect = datetime.datetime(year=2024, month=1, day=19, hour=00, minute=00, second=00)
        result = map_value(value=value, to_type = Types.DATETIME)
        assert result == expect

if __name__ == '__main__':
    pytest.main()