try:
    import requests

except Exception as e:
    print(f"Some modules are missing: {e}")


def json_data(url):
    """
    Simple method to use requests in order to jsonify whatever URL data I'm given, This is poorly worded so I should update this
    """
    r = requests.get(url)
    txt = r.json()
    return txt
