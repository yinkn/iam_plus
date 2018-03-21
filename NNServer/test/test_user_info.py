import unittest

import sys
import os
import logging
import time

import sqlite3

sys.path.append("../src")

from user_info import UserInfo

class TestUserInfo(unittest.TestCase):

    user_info = UserInfo()

    def setUp(self):
        FORMAT = "%(asctime)-15s %(message)s"
        logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    def tearDown(self):
        pass

    def test_user_info_operation(self):
        logging.info("test_user_info_operation:")
        sqlite_file = "user_info_test.db"
        user_name = "user1"
        if os.path.isfile(sqlite_file):
            os.remove(sqlite_file)

        self.user_info.init_sqlite(sqlite_file)        
        self.assertEqual(os.path.isfile(sqlite_file), True)

        self.user_info.user_register(user_name, "1234asdf", "user1@demo.com", {'a': 1})

        result = self.user_info.user_login(user_name, "1234asdf")
        self.assertEqual(result, True)
        
        self.user_info.exit_sqlite()

        # reopen db
        self.user_info.init_sqlite(sqlite_file)    
            
        self.assertEqual(os.path.isfile(sqlite_file), True)
        result = self.user_info.user_login(user_name, "1234asdf")
        self.assertEqual(result, True)
        
        self.user_info.exit_sqlite()

        # open db directly
        con = sqlite3.connect(sqlite_file)
        cur = con.cursor()
        # And this is the named style:
        cur.execute("select user_name from user_info where user_name=?", (user_name,))
        user = cur.fetchone()
        self.assertEqual(user[0], user_name)
        con.close()

    def test_get_typing_record_with_kv(self):
        logging.info("test_get_typing_record_with_kv:")
        sqlite_file = "user_info_test.db"
        user_name = "test"
        password = "test1234"
        if os.path.isfile(sqlite_file):
            os.remove(sqlite_file)

        self.user_info.init_sqlite(sqlite_file)        
        self.assertEqual(os.path.isfile(sqlite_file), True)

        self.user_info.user_register(user_name, password, "user1@demo.com", {'a': 1})

        result = self.user_info.user_login(user_name, password)
        self.assertEqual(result, True)

        type_record = [-52, -101, -30, 955, 172, 185, 1297]
        self.user_info.user_typing_record(user_name, str(type_record), {'time':int(time.time()), "tag":1})

        type_record = [-32, -151, -48, 700, 164, 169, 191]
        self.user_info.user_typing_record(user_name, str(type_record), {'time':int(time.time()), "tag":1})

        record_list = self.user_info.get_typing_record_with_kv(user_name, {"tag":1})

        self.assertEqual(len(record_list), 2)
        self.assertEqual(str([-52, -101, -30, 955, 172, 185, 1297]) in record_list, True)
        self.assertEqual(str([-32, -151, -48, 700, 164, 169, 191]) in record_list, True)
        
        self.user_info.exit_sqlite()


if __name__ == '__main__':
    unittest.main()