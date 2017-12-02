import unittest

import sys
import os

sys.path.append("../src")

from user_info import UserInfo

class TestUserInfo(unittest.TestCase):

    user_info = UserInfo()

    def test_user_info_operation(self):
        sqlite_file = "user_info_test.db"
        if os.path.isfile(sqlite_file):
            os.remove(sqlite_file)

        self.user_info.init_sqlite(sqlite_file)        
        self.assertEqual(os.path.isfile(sqlite_file), True)

        self.user_info.user_register("user1", "1234asdf", "user1@demo.com", {'a': 1})

        result = self.user_info.user_login("user1", "1234asdf")
        self.assertEqual(result, True)
        
        self.user_info.exit_sqlite()



if __name__ == '__main__':
    unittest.main()