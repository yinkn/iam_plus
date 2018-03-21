#!/root/hackathon/flask/bin/python

import logging
import time

from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS, cross_origin

from user_info import UserInfo
from keras_seq import KerasModelMgr

app = Flask(__name__)

cors = CORS(app)

#user info db
user_info = UserInfo()
sqlite_file = "user_info_sqlite.db"

keras_model_mgr = KerasModelMgr()

def get_user_info_db():
    if user_info.is_connected():
        return user_info
    else:
        user_info.init_sqlite(sqlite_file)
        return user_info

@app.route('/register', methods=['POST'])
def register():
    logging.debug("register: " + str(request))
    userName = request.json["userName"]
    password = request.json["password"]
    logging.info("register: " + str(userName))
    logging.debug("register: " + str(request.json))
    user_info_db = get_user_info_db()
    if user_info_db.user_is_existing(userName) is False:
        user_info_db.user_register(userName, password, "", {})
        for type_record in request.json["dataset"]:
            user_info_db.user_typing_record(userName, str(type_record), {'time':int(time.time()), "tag":1})
    else:
        logging.info("register: {0} is exist.".format(userName))
    return '', 200


@app.route('/login', methods=['POST'])
def login():
    logging.debug("login: " + str(request))
    userName = request.json["userName"]
    password = request.json["password"]
    logging.info("login: " + str(userName))
    logging.debug("login: " + str(request.json))
    user_info_db = get_user_info_db()
    result = user_info_db.user_login(userName, password)

    if result is True:
        testX = []
        for type_record in request.json["dataset"]:
            user_info_db.user_typing_record(userName, str(type_record), {'time':int(time.time())}) 
            testX.append(type_record)       
        rate = keras_model_mgr.predict(userName, testX)
        response = {"rate": rate}
        return jsonify(response), 200
    else:
        return jsonify(response), 404

@app.route('/train', methods=['POST'])
def train():
    logging.debug("train: " + str(request))
    userName = request.json["userName"]
    password = request.json["password"]
    logging.info("login: " + str(userName))
    logging.debug("login: " + str(request.json))
    user_info_db = get_user_info_db()
    result = user_info_db.user_login(userName, password)

    if result is True:
        record_list_1 = user_info_db.get_typing_record_with_kv(userName,{'tag':1})
        record_list_2 = user_info_db.get_typing_record_with_kv(userName,{'tag':0})
        keras_model_mgr.train(userName, record_list_1, record_list_2)
        return "Training completed.", 200
    else:
        return "Can't login for training", 404

def init_log():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=FORMAT)

if __name__ == '__main__':
    init_log()
    logging.info("APP starting...")
    app.run(debug=True)


