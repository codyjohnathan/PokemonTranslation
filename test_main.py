try:
    import unittest
    import pytest
    import requests

except Exception as e:
    print(f"Some modules are missing: {e}")

# this code stops the need to turn the project folder into a package
target = __import__("app_run.py")
app = target.app


"""
Notes on unittest:
-  unittest requires you put your tests in classes as methods
- You use a series of special assertion methods in the unittest.TestCase class instead of the built-in assert statement
"""

apiBase = "http://127.0.0.1:5000/"

response = requests.get(apiBase + "/pokemon/charizard/")
print(response.json())

# checking if response of 200 is returned


class Test_functionality(unittest.TestCase):

    def test_healthcheck_PokeAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/")
        status_code = response.status_code
        assert status_code == 200

        # the status code should be a redirect i.e. 300; so I made a separate test for this

    def test_healthcheck_ShakesprAPI(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        assert response.status_code == 308

    def test_response_content(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        assert response.content_type == 'application/json'

    def test_trans_shakespeare_response(self):
        manualtest = app.test_client(self)
        response = manualtest.get("/pokemon/charizard")
        assert b"doth" in response.data


if __name__ == "__main__":
    unittest.main()  # Command line entry point : This executes the test runner by discovering all classes in this file that inherit from unittest.TestCase
