import requests


def get_static(**par):
    static_api = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(static_api, params=par)

    return response.content


def search(**par):
    search_api = "https://search-maps.yandex.ru/v1/"

    api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
    par['apikey'] = api_key

    response = requests.get(search_api, params=par)

    return


def get_org(json_data):
    return json_data["features"]


def get_toponym(json_data):
    return json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_t_coords(toponym):
    return list(map(float, toponym['Point']['pos'].split(' ')))


def get_spn(toponym):
    lc1, lc2 = map(float, toponym['boundedBy']['Envelope']['lowerCorner'].split())
    uc1, uc2 = map(float, toponym['boundedBy']['Envelope']['upperCorner'].split())
    return uc1 - lc1, uc2 - lc2


def geocode(name):
    geocode_api = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }

    response = requests.get(geocode_api, params=geocoder_params)

    if not response:
        print('Error {0} {1}'.format(response.status_code, response.reason))
        exit(-1)

    return response.json()


def get_org_info(organization):
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_hours = organization["properties"]["CompanyMetaData"]["Hours"]
    return org_name, org_address, org_hours


def get_org_pos(organization):
    point = organization["geometry"]["coordinates"]
    return list(map(float, point))
