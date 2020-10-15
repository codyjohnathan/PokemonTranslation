import unittest

import requests

from PokemonTranslation.app_run import app

# import APIscraping as API_scrape

BASE = "http://127.0.0.1:5000/"

response = requests.get(BASE + "/pokemon/clefairy/")
print(response.json())


class Flasktest(unittest.TestCase):

    # checking if response of 200 is returned
    def test_healthcheck_PokeAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get(BASE + "/pokemon/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_healthcheck_ShakespeAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get(BASE + "/pokemon/charizard")
        status_code = response.status_code
        self.assertEqual(status_code, 308)


if __name__ == "__main__":
    unittest.main()
