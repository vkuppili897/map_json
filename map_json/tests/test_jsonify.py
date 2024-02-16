import os
import sys
import pytest


base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lambda_path = os.path.join(base_path, 'code')
sys.path.append(lambda_path)

from jsonify import jsonify

class TestJsonify:

    def test_get(self):

        data = [{
            "a": "b",
            "c": [1,2],
            "d": (1, 2)
        }]

        key = "[0].{d}.(0)"
        data = jsonify(data=data)
        mapped_dict = data.get(keystr=key, default=None, return_default=True)
        assert mapped_dict == {"0": 1}

print("testing TestJSONMapper")

if __name__ == '__main__':
    pytest.main()
