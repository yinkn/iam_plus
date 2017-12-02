
import time

def str_to_dict(str):
    pass

def dict_to_str(key_value={}):
    kv_str = ""
    for k in key_value.keys():
        kv_str = "{0}={1},".format(k,key_value[k])
    
    return kv_str.strip(",")

def time_to_str(secs=None):
    "Exapmle: 2017-12-02 08:05:39 UTC"
    return time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(secs))
