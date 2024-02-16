import os
import sys
import pytest


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
code_dir_path = os.path.join(base_path, 'code')
sys.path.append(code_dir_path)

from json_mapper import map, Types

class TestJSONMapper:

    def test_map(self):

        data = [{
            "a": "b",
            "c": [1,2],
            "d": (1, 2)
        }]

        key = "[0].{d}.(0)"

        mapped_dict = map(data=data, key=key, to_type=Types.DECIMAL, split_by = ".", default=None, return_default=False)
        
        assert mapped_dict == {"0": 1.0}


if __name__ == '__main__':
    pytest.main()
