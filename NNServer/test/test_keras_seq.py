import unittest
import sys

import numpy
from numpy import *

sys.path.append("../src")

from keras_seq import KerasModelMgr

class TestKerasSeq(unittest.TestCase):

    def test_train_predict_1(self):
        kmMgr = KerasModelMgr()
        userName = "demo1"
        trainX1input = [
            [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
            [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
            [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]]
        trainX2input = [
            [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
            [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
            [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]]
        kmMgr.train(userName, trainX1input, trainX2input)
        testX = array([
            [120, 120, 200, 120, 110, 130, 140, 120, 130, 120]])
        rate = kmMgr.predict(userName, testX)

        self.assertEqual(rate * 100 > 80, True)

    def test_train_predict_2(self):
        kmMgr = KerasModelMgr()
        userName = "demo1"
        trainX1input = [
            [120, 120, 200, 120, 110, 130, 140, 120, 130, 120],
            [200, 150, 250, 180, 150, 180, 180, 200, 200, 180],
            [220, 190, 300, 220, 180, 210, 220, 280, 270, 240]]
        trainX2input = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        kmMgr.train(userName, trainX1input, trainX2input)
        testX = [
            [120, 120, 200, 120, 110, 130, 140, 120, 130, 120]]
        rate = kmMgr.predict(userName, testX)

        self.assertEqual(rate * 100 > 80, True)


if __name__ == '__main__':
    unittest.main()