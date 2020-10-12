import unittest

import requests

from app_run import app

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/pokemon/clefairy" )
print(response.json())

class Flasktest(unittest.TestCase):

    #checking if response of 200 is returned
    def healthcheck(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/clefairy")
        status_code = response.status_code
        self.assertEqual(status_code, 200)


    # check content is application/json
    def json_app_check(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/<string: name>")
        self.assertEqual(response.content_type, "application/json")

    #check for data returned
    def returned_data_check(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/<string: name>")
        self.assertTrue('description' in response.data)

    if __name__=="__main__":
        unittest.main()
