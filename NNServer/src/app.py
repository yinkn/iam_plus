#!/root/hackathon/flask/bin/python

import logging

from flask import Flask, jsonify, request
from flask import Response
from flask_cors import CORS, cross_origin
import numpy
from numpy import *
from keras.models import Sequential, load_model
from keras.layers import Dense


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
    return '', 200

def train():
    userName = request.json["userName"]
    print(userName)

    # Get Input Features and Calculate Mean Vaule and Standard Deviation
    trainX1input = numpy.array(request.json["dataset"])
    print(trainX1input)
    #trainX1input = array([
    #       [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
    #       [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
    #       [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]])
    trainX1inputmean  = numpy.mean(trainX1input,axis=0)
    trainX1inputsigma = numpy.std(trainX1input,axis=0)

    trainX2input = numpy.array(request.json["dataset2"])
    print(trainX2input)
    #trainX2input = array([
    #       [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
    #       [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
    #       [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]])
    trainX2inputmean  = numpy.mean(trainX2input,axis=0)
    trainX2inputsigma = numpy.std(trainX2input,axis=0)

    dim = trainX1input.shape[1]

    # Generate Training Set
    X1 = numpy.random.normal(trainX1inputmean, trainX1inputsigma, (100, dim))
    X2 = numpy.random.normal(trainX2inputmean, trainX2inputsigma, (200, dim))
    trainX = numpy.vstack((X1, X2))

    Y1 = numpy.ones(100, dtype=numpy.int)
    Y2 = numpy.zeros(200, dtype=numpy.int)
    trainY = numpy.hstack((Y1, Y2))

    print(trainX)
    print(trainY)
    print(dim)

    # Create Model
    model = Sequential()
    model.add(Dense(dim, input_dim=dim, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='sigmoid'))

    # Compile Model
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Fit Model
    model.fit(trainX, trainY, epochs=1000, batch_size=10)

    # Evaluate Model
    scores = model.evaluate(trainX, trainY)

    print("   ")
    print("   ")
    print("   ====== IAM+ DEMO =======   ")
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

    model.save('%s.h5' % str(userName))

    return '', 200



def predict():
    userName = request.json["userName"]

    model = load_model("%s.h5" % str(userName))

    testX = numpy.array(request.json["dataset"])
    predictions = model.predict(testX)
    response = {"rate": predictions.item(0)}
    return jsonify(response), 200

def init_log():
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(level=logging.DEBUG,format=FORMAT)

if __name__ == '__main__':
    init_log()
    logging.info("APP starting...")
    app.run(debug=True)


