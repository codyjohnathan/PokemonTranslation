import unittest

import requests

from app_run import app

# import APIscraping as API_scrape

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/pokemon/clefairy/")
print(response.json())


class Flasktest(unittest.TestCase):

    # checking if response of 200 is returned
    def test_healthcheck(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/clefairy")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    if __name__ == "__main__":
        unittest.main()
