"""
Fetch multi-model forecasts for ~40 US cities from Open-Meteo and save data/forecast.json.
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone

CITIES = [
    ("Phoenix", 33.45, -112.07), ("Seattle", 47.61, -122.33), ("Portland", 45.52, -122.68),
    ("San Francisco", 37.77, -122.42), ("Los Angeles", 34.05, -118.24), ("San Diego", 32.72, -117.16),
    ("Las Vegas", 36.17, -115.14), ("Salt Lake City", 40.76, -111.89), ("Boise", 43.62, -116.20),
    ("Denver", 39.74, -104.99), ("Albuquerque", 35.08, -106.65), ("El Paso", 31.76, -106.49),
    ("Billings", 45.78, -108.50), ("Cheyenne", 41.14, -104.82), ("Bismarck", 46.81, -100.78),
    ("Rapid City", 44.08, -103.23), ("Omaha", 41.26, -95.93), ("Kansas City", 39.10, -94.58),
    ("Oklahoma City", 35.47, -97.52), ("Dallas", 32.78, -96.80), ("Houston", 29.76, -95.37),
    ("San Antonio", 29.42, -98.49), ("New Orleans", 29.95, -90.07), ("Minneapolis", 44.98, -93.27),
    ("Chicago", 41.88, -87.63), ("St. Louis", 38.63, -90.20), ("Memphis", 35.15, -90.05),
    ("Nashville", 36.16, -86.78), ("Detroit", 42.33, -83.05), ("Indianapolis", 39.77, -86.16),
    ("Atlanta", 33.75, -84.39), ("Birmingham", 33.52, -86.80), ("Miami", 25.76, -80.19),
    ("Tampa", 27.95, -82.46), ("Charlotte", 35.23, -80.84), ("Washington DC", 38.91, -77.04),
    ("Philadelphia", 39.95, -75.17), ("New York", 40.71, -74.01), ("Boston", 42.36, -71.06),
    ("Pittsburgh", 40.44, -80.00), ("Buffalo", 42.89, -78.88), ("Anchorage", 61.22, -149.90),
    ("Honolulu", 21.31, -157.86),
]

MODELS = ["gfs_seamless", "ecmwf_ifs025", "icon_seamless", "gem_seamless"]
VARS = ["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "precipitation", "snowfall"]
CHUNK = 14  
API = "https://api.open-meteo.com/v1/forecast"


def fetch_chunk(chunk):
    params = {
        "latitude": ",".join(str(c[1]) for c in chunk),
        "longitude": ",".join(str(c[2]) for c in chunk),
        "hourly": ",".join(VARS),
        "models": ",".join(MODELS),
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch",
        "timezone": "GMT",
        "forecast_days": 7,
    }
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                out = json.load(resp)
            return out if isinstance(out, list) else [out]
        except Exception as exc: 
            print(f"  attempt {attempt + 1} failed: {exc}")
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("Open-Meteo request failed after retries")


def main():
    locations = []
    for i in range(0, len(CITIES), CHUNK):
        chunk = CITIES[i:i + CHUNK]
        print(f"Fetching {chunk[0][0]} ... {chunk[-1][0]}")
        for (name, lat, lon), result in zip(chunk, fetch_chunk(chunk)):
            hourly = result["hourly"]
            locations.append({
                "name": name, "lat": lat, "lon": lon,
                "time": hourly["time"],  # UTC
                "data": {v: {m: hourly.get(f"{v}_{m}") for m in MODELS} for v in VARS},
            })
        time.sleep(1)

    out = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="minutes"),
        "models": MODELS,
        "locations": locations,
    }
    path = pathlib.Path("data/forecast.json")
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, separators=(",", ":")))
    print(f"Wrote {path} ({path.stat().st_size / 1e6:.1f} MB)")


if __name__ == "__main__":
    main()
