try:
    from app_run import app
    import unittest

    import requests

except Exception as e:
    print(f"Some modules are missing: {e}")


# import APIscraping as API_scrape

apiBase = "http://127.0.0.1:5000/"

response = requests.get(apiBase + "/pokemon/charizard/")
print(response.json())


class Test_functions(unittest.TestCase):

    # checking if response of 200 is returned
    def test_healthcheck_PokeAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    # the status code should be a redirect i.e. 300; so I made a separate test for this
    def test_healthcheck_ShakespeAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        status_code = response.status_code
        self.assertEqual(status_code, 308)

    def test_json_data(self):
        manualtest = app.test_client(self)
        response = manualtest.get(apiBase + "/pokemon/charizard")
        self.assertEqual(response.content_type,
                         'application/json; charset=utf-8; text/html')

    def test_trans_shakespeare_response(self):
        manualtest = app.test_client(self)
        response = manualtest.get(apiBase + "/pokemon/charizard")
        self.assertFalse(b"doth" in response.data)


if __name__ == "__main__":
    unittest.main()
