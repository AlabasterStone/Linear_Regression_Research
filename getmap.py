import requests
#调用腾讯地图Web Service API
from haversine import haversine

API_SEARCH_URL = "https://apis.map.qq.com/ws/place/v1/search"
API_EXPLORE_URL = "https://apis.map.qq.com/ws/place/v1/explore"
API_KEY = "OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77"
POINT_TIANANMEN: tuple = (39.908823, 116.39747)


def get_place_location(keyword: str) -> tuple | bool:
    res = requests.get(API_SEARCH_URL, params={
        "boundary": "region(北京, 0)",
        "page_size": 1,
        "page_index": 1,
        "keyword": keyword,
        "filter": "category=住宅小区",
        "key": API_KEY
    }, headers={
        "Referer": "https://lbs.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
    }).json()
    if res["message"] == "query ok":
        if res["count"] == 0:
            return False
        else:
            return res["data"][0]["location"]["lat"], res["data"][0]["location"]["lng"]
    else:
        raise RuntimeError(res["status"], res["message"])

#return count,nearest distance


def get_subway_count_and_distance(lat, lng) -> tuple | bool:
    res = requests.get(API_EXPLORE_URL, params={
        "boundary": f"nearby({lat},{lng},1000,0)",
        "page_size": 20,
        "page_index": 1,
        "policy": 2,
        "orderby": "_distance",
        "filter": "category=地铁站",
        "key": API_KEY
    }, headers={
        "Referer": "https://lbs.qq.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52"
    }).json()
    if res["message"] == "query ok":
        if(res["count"]==0):
            return False
        else:
            return res["count"], res["data"][0]["_distance"]
    else:
        raise RuntimeError(res["status"], res["message"])


def get_center_distance(point1: tuple, point2: tuple) -> float:
    return haversine(point1, point2)
