import requests


API_URL = "https://api.truckersmp.com/v2"

TIMEOUT = 15


def request(endpoint):
    url = f"{API_URL}{endpoint}"

    try:
        response = requests.get(
            url,
            timeout=TIMEOUT,
        )

        print(
            f"TruckersMP API: "
            f"{response.status_code} {url}"
        )

        response.raise_for_status()

        data = response.json()

        if data.get("error") is True:
            print(
                f"TruckersMP API returned error: {data}"
            )
            return None

        return data

    except requests.RequestException as error:
        print(
            f"TruckersMP request error: {error}"
        )

        return None

    except ValueError as error:
        print(
            f"TruckersMP JSON error: {error}"
        )

        return None


def get_servers():
    data = request("/servers")

    if data is None:
        return None

    return data.get("response")


def get_game_time():
    data = request("/game_time")

    if data is None:
        return None

    return data.get("game_time")
    

def get_version():
    return request("/version")


def get_events():
    return request("/events")


def get_rules():
    return request("/rules")
