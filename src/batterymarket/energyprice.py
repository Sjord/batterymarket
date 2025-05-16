import requests
from datetime import datetime, timedelta, UTC
from zoneinfo import ZoneInfo
import json
import subprocess
import os
from math import sqrt


def main():
    tz_ams = ZoneInfo("Europe/Amsterdam")

    today = datetime.now(tz=tz_ams).replace(hour=0, minute=0, second=0, microsecond=0)
    tomorrow = today + timedelta(days=1)

    date_str = today.strftime("%Y-%m-%d")
    cache_path = f"/Users/sjoerd/dev/batterymarket/prices/{date_str}.json"

    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            data = json.load(f)
    else:
        from_time = today.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        to_time = tomorrow.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z")

        url = "https://newtransparency.entsoe.eu/market/energyPrices/load"
        payload = {
            "areaList": ["BZN|10YNL----------L"],
            "dateTimeRange": {
                "from": from_time,
                "to": to_time,
            },
            "filterMap": {},
            "intervalPageInfo": {"itemIndex": 0, "pageSize": 10},
            "sorterList": [],
            "timeZone": "CET",
        }
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "https://github.com/Sjord/batterymarket",
        }

        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        with open(cache_path, "w") as f:
            json.dump(data, f, indent=2)

        print(date_str)

    prices = data["instanceList"][0]["curveData"]["periodList"][0]["pointMap"]
    curhour = datetime.now(tz=tz_ams).hour
    curprice = float(prices[str(curhour)][0])
    pricelist = [float(p[0]) for p in prices.values()]
    maxprice = max(pricelist)
    minprice = min(pricelist)
    ratio = (curprice - minprice) / (maxprice - minprice)
    batterylevel = int(100 - 50 * sqrt(ratio))

    print(
        f"hour: {curhour} price: {curprice}, min: {minprice}, max: {maxprice}, ratio: {ratio}, batterylevel: {batterylevel}"
    )
    subprocess.run(["/usr/local/bin/bclm", "write", str(batterylevel)])


if __name__ == "__main__":
    main()
