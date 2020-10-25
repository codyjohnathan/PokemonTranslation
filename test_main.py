try:
    import unittest
    import requests
    target = __import__("main.py")
    app = target.app  # this code stops the need to turn the project folder into a package

except Exception as e:
    print(f"Some modules are missing: {e}")

"""
Notes on unittest:
-  unittest requires you put your tests in classes as methods
- You use a series of special assertion methods in the unittest.TestCase class instead of the built-in assert statement
"""

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
    def test_healthcheck_ShakesprAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        self.assertEqual(response.status_code, 308)

    def test_response_content(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        self.assertEqual(response.content_type,
                         'text/html; application/json')

    def test_trans_shakespeare_response(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        self.assertTrue(b"doth" in response.data)


if __name__ == "__main__":
    unittest.main()
