"""
curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/train   -d '{"userName":"TEST1","dataset":[[-15, -57, 88, 50, 16, 83, 198, 16, -70],[202, -53, 140, 134, 0, 84, 165, -16, -15],[15, -67, 96, 108, 0, 79, 212, -16, -23],[16, -67, 126, 119, -15, 67, 258, -16, -16],[53, -65, 155, 59, 15, 65, 179, -16, 15],[56, -68, 104, 137, -16, 88, 382, 16, -70]], "dataset2":[[41, -47, 1065, -15, 85, 181, 892, 16, -15],[15, -15, 922, 164, 80, 488, 302, 67, 51],[448, 1770, 2118, 1348, 495, 117, 1286, 430, 633],[47, -34, 1405, 75, 49, 228, 1115, 89, 16],[550, 1080, 383, 321, 97, 350, 1420, 43, 1114],[89, 430, 1034, 97, 36, 112, 387, 57, 16]]}' 
curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/predict -d '{"userName":"DEMO1","dataset":[[200,27,102,80,-36,80,579,66,21,61,208,71,-110]]}'
"""

"""
curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/register   -d '{"userName":"TEST1","dataset":[[-15, -57, 88, 50, 16, 83, 198, 16, -70],[202, -53, 140, 134, 0, 84, 165, -16, -15],[15, -67, 96, 108, 0, 79, 212, -16, -23],[16, -67, 126, 119, -15, 67, 258, -16, -16],[53, -65, 155, 59, 15, 65, 179, -16, 15],[56, -68, 104, 137, -16, 88, 382, 16, -70]], "dataset2":[[41, -47, 1065, -15, 85, 181, 892, 16, -15],[15, -15, 922, 164, 80, 488, 302, 67, 51],[448, 1770, 2118, 1348, 495, 117, 1286, 430, 633],[47, -34, 1405, 75, 49, 228, 1115, 89, 16],[550, 1080, 383, 321, 97, 350, 1420, 43, 1114],[89, 430, 1034, 97, 36, 112, 387, 57, 16]]}' 
curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/login -d '{"userName":"DEMO1","dataset":[[200,27,102,80,-36,80,579,66,21,61,208,71,-110]]}'
curl -i -X POST -H "Content-Type:application/json" http://localhost:5000/train   -d '{"userName":"test3", "password":""}'
"""

import os
import sys
import unittest
import json
import logging


sys.path.append("../src")

import app

class FlaskAppTest(unittest.TestCase):

    def setUp(self):
        self.client = app.app.test_client()

    def tearDown(self):
        pass

    def test_register_login(self):
        logging.debug("test_login:")
        response = self.client.post('/register', 
        data=json.dumps({"userName":"DEMO1", "password":"12345","dataset":[[200,27,102,80,-36,80,579,66,21,61,208,71,-110],[200,27,102,80,-36,80,579,66,21,61,208,71,-110]]})
        , content_type='application/json'
        , follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        logging.debug("test_login:")
        response = self.client.post('/login', 
        data=json.dumps({"userName":"DEMO1", "password":"12345","dataset":[[200,27,102,80,-36,80,579,66,21,61,208,71,-110],[200,27,102,80,-36,80,579,66,21,61,208,71,-110]]})
        , content_type='application/json'
        , follow_redirects=True)
        self.assertEqual(response.status_code, 200)
    

if __name__ == '__main__':
    app.init_log()
    unittest.main()