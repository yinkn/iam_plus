import unittest

import sys

sys.path.append("../src")

from util import dict_to_str
from util import time_to_str

class TestUtil(unittest.TestCase):

    def test_dict_to_str(self):
        key_value = {}
        key_value["a"]="1"
        kv_str = "a=1"
        print(kv_str)
        self.assertEqual(kv_str, dict_to_str(key_value))

    def test_time_to_str(self):
        now_secs = 1512202121.623
        now_str = "2017-12-02 08:08:41 UTC"        
        print(now_str)
        self.assertEqual(now_str, time_to_str(now_secs))

if __name__ == '__main__':
    unittest.main()