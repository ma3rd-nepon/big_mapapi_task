import requests


def get_response(type_of_response, api, **par):
    urls = {
        'static': "http://static-maps.yandex.ru/1.x/",
        'geocode': "http://geocode-maps.yandex.ru/1.x/",
        'search': "https://search-maps.yandex.ru/v1/"
    }

    if api == 'search':
        api_key = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
        par['apikey'] = api_key

    response = requests.get(urls[api], params=par)
    if not response:
        print('Error {0} {1}'.format(response.status_code, response.reason))
        print(api)
        exit(-1)

    if type_of_response == 'json':
        return response.json()

    if type_of_response == 'content':
        return response.content


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


def get_org_info(organization):
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    org_hours = organization["properties"]["CompanyMetaData"]["Hours"]
    return org_name, org_address, org_hours


def get_org_pos(organization):
    point = organization["geometry"]["coordinates"]
    return list(map(float, point))
