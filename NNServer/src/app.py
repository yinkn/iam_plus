#!/root/hackathon/flask/bin/python

import logging

from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS, cross_origin



app = Flask(__name__)

cors = CORS(app)

@app.route('/register', methods=['POST'])
def register():
    logging.debug("register: " + str(request))
    userName = request.json["userName"]
    logging.info("register: " + str(userName))
    logging.debug("register: " + str(request.json))
    return '', 200


@app.route('/login', methods=['POST'])
def login():
    logging.debug("login: " + str(request))
    userName = request.json["userName"]
    logging.info("login: " + str(userName))
    logging.debug("login: " + str(request.json))
    response = {"rate": 100}
    return jsonify(response), 200

def init_log():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=FORMAT)

if __name__ == '__main__':
    init_log()
    logging.info("APP starting...")
    app.run(debug=True)


