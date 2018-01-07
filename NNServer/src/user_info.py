
"""
UserInfo:
| user_name | password | e_mail         | register_time| key_value               |
| demo1     | ****     | demo1@demo.com | 2017-11-30   | key1=value1;key2=value2 |

UserRecord:
|user_name  | record_time               | typing_record                                   | key_value               |
|demo1      | 2017-11-30  07:11:00      | [200,27,102,80,-36,80,579,66,21,61,208,71,-110] | key1=value1;key2=value2 |

CREATE TABLE user_info (user_name text, password text, e_mail text, register_time text, key_value text)
CREATE TABLE user_record (user_name user_name, record_time text, typing_record text, key_value text)


"""
import os
import sqlite3

import util

import logging

class UserInfo:
    """class to handle user information"""

    sqlite_conn = None

    def is_connected(self):
        if self.sqlite_conn is None:
            return False
        else:
            return True

    def init_sqlite(self, data_file):
        if os.path.isfile(data_file):
            logging.info("Connect sqlite {0}".format(data_file))
            self.sqlite_conn = sqlite3.connect(data_file)
        else:
            #if data_file is not existing, the connect will create one
            logging.info("Create sqlite {0}".format(data_file))
            self.sqlite_conn = sqlite3.connect(data_file)
            cur = self.sqlite_conn.cursor()
            sql = "CREATE TABLE user_info (name_id integer primary key, user_name text, password text, e_mail text, register_time text, key_value text)"
            cur.execute(sql)
            sql = "CREATE TABLE user_record (record_id integer primary key, user_name user_name, record_time text, typing_record text, key_value text)"
            cur.execute(sql)
            #commit db change
            self.sqlite_conn.commit()

    def exit_sqlite(self):
        if self.sqlite_conn != None:
            self.sqlite_conn.close()
            self.sqlite_conn = None

    def user_register(self, user_name, password, e_mail, key_value={}):
        result = False
        description = "Unknow reason."

        if self.user_is_existing(user_name.strip()) == True:
            result = False
            description = "User is existing."
            logging.debug("[{0}] user is created before registration.")
        else:
            now_time = util.time_to_str()
            kv_str = util.dict_to_str(key_value)
            cur = self.sqlite_conn.cursor()
            cur.execute("insert into user_info(user_name, password, e_mail, register_time, key_value) values (?, ?, ?, ?, ?)"
                , (user_name.strip(), password.strip(), e_mail.strip(), now_time, kv_str))
            #commit data change
            self.sqlite_conn.commit()
            result = True
            description = "User is created."
            logging.info("[{0}] user is created.".format(user_name))
       
        return result, description

    def user_login(self, user_name, password):
        cur = self.sqlite_conn.cursor()
        cur.execute('select user_name from user_info where user_name=? and password=?', (user_name, password))
        user = cur.fetchone() 
        if user is None:
            return False
        else:
            return True
            logging.info("[{0}] user login.".format(user_name))

    def user_typing_record(self, user_name, typing, key_value={}):
        result = False
        description = "Unknow reason."

        if self.user_is_existing(user_name.strip()) == True:
            now_time = util.time_to_str()
            kv_str = util.dict_to_str(key_value)
            cur = self.sqlite_conn.cursor()
            cur.execute("insert into user_record(user_name, record_time, record_time, key_value) values (?, ?, ?, ?)"
                , (user_name.strip(), typing.strip(), now_time, kv_str))
            #commit data change
            self.sqlite_conn.commit()
            result = True
            description = "Data is record."
        else:
            result = False
            description = "User is not existing."
       
        return result, description

    def user_logout(self, user_name):
        pass

    def user_unregister(self, user_name):
        pass

    def user_is_existing(self, user_name):
        cur = self.sqlite_conn.cursor()
        cur.execute('select user_name from user_info where user_name=?', (user_name, ))
        user = cur.fetchone()
        #logging.debug("user_is_existing: {0}".format(user))
        if user is None:
            return False
        else:
            return True
