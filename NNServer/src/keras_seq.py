import numpy
from numpy import *
from keras.models import Sequential, load_model
from keras.layers import Dense

class KerasModelMgr:
    """class to handle user information"""

    def __init__(self):
        self.model_map = {}

    def train(self, userName, trainX1input, trainX2input):
        """
        trainX1input: positive input
        trainX2input: negative input
        """
        # userName = request.json["userName"]
        # print(userName)

        # Get Input Features and Calculate Mean Vaule and Standard Deviation
        # trainX1input = numpy.array(request.json["dataset"])
        print(trainX1input)
        #trainX1input = array([
        #       [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
        #       [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
        #       [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]])
        trainX1input = array(trainX1input)
        trainX2input = array(trainX2input)

        trainX1inputmean  = numpy.mean(trainX1input,axis=0)
        trainX1inputsigma = numpy.std(trainX1input,axis=0)

        #trainX2input = numpy.array(request.json["dataset2"])
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
        print("   ====== train =======   ")
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

        model.save('%s.h5' % str(userName))


    def predict(self, userName, testX):
        #userName = request.json["userName"]
        if userName not in self.model_map:
             model = load_model("%s.h5" % str(userName))
             self.model_map[userName] = model

        model = self.model_map[userName]

        #testX = numpy.array(request.json["dataset"])
        testX = array(testX)
        predictions = model.predict(testX)
        return predictions.item(0)
