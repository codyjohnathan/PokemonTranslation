import requests


def clean_text(txt):
    clean = txt.replace("\n", " ")
    return clean


def extract_descriptive_text(json_blob, language='en', version='sword'):
    """
    Parses through nested dictionary from Poke API and grabs all flavor text entries
    that are in english and come from the latest Pokemon game, Sword, in order to
    get the most up to date info
    :param json_blob:
    :param language:
    :param version:
    :return:
    """
    text = ""
    for f in json_blob['flavor_text_entries']:
        if f['language']['name'] == language and f['version']['name'] == version:
            text = f['flavor_text']
    return text


def json_data(url):
    r = requests.get(url)
    txt = r.json()
    return txt
