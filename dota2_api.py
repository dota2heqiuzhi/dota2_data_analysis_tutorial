import requests

def get_api_json(url):
    try:
        r = requests.get(url, timeout=3)
        r_json = r.json()
        return r_json
    except:
        return get_api_json(url)

if __name__ == '__main__':
    pass
