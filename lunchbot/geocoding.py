import requests
import math


def geocode(query):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"format": "json", "q": query}
    headers = {
        "User-Agent": "Lunchbot-Geocoder/0.1 (+https://github.com/sotander/lunchbot; contact: ondrej@sotander.com)",
        "Referer": "https://github.com/sotander/lunchbot"
    }
    r = requests.get(url, params=params, headers=headers)
    try:
        data = r.json()
    except requests.exceptions.JSONDecodeError:
        print(r)
        raise r
    if not data:
        return None
    return float(data[0]["lat"]), float(data[0]["lon"])


def haversine(lat1, lon1, lat2, lon2):
    ''' https://en.wikipedia.org/wiki/Haversine_formula'''
    R = 6371.0  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def is_within_km(km, base_lat, base_lon, other_lat, other_lon):
    dist = haversine(base_lat, base_lon, other_lat, other_lon)
    return dist <= km, dist
