import time

import requests

BASE_URL = "http://localhost:5000/api/"
BASE_HEADER = {"Content-Type": "application/json"}


def jwt_error_handler(response: requests.Response):
    if response.status_code == 401:
        pass


def _send_request(method, url: str, **kwargs) -> [requests.Response, str]:
    json = kwargs.get("json")

    header, access_token, refresh_token = _prepare_header(kwargs)

    response = method(BASE_URL + url, headers=header, json=json)
    print(url)
    print(header)
    print(json)
    print(f"{response.status_code}: {response.json()}")
    print()
    if response.status_code == 401 and response.json().get("msg") == "Token has expired":
        response, access_token = _send_request(requests.get, "/auth/refresh", refresh_token=refresh_token)
        access_token = response.json().get("access_token")
        kwargs["access_token"] = access_token
        _send_request(method, url, **kwargs)

    return response, access_token


def _prepare_header(kwargs):
    access_token = kwargs.get("access_token")
    refresh_token = kwargs.get("refresh_token")
    header = BASE_HEADER.copy()
    if access_token is not None:
        header["Authorization"] = f"Bearer {access_token}"
    elif refresh_token is not None:
        header["Authorization"] = f"Bearer {refresh_token}"
    return header, access_token, refresh_token


def login() -> [str, str]:
    login_data = {"username": "both", "password": "1234"}
    response, foo = _send_request(requests.post, "auth/login", json=login_data)
    json_response = response.json()
    return json_response["access_token"], json_response["refresh_token"]


def refresh_login(refresh_token: str) -> str:
    response = requests.get(
        'http://localhost:5000/api/auth/refresh',
        headers={"Authorization": "Bearer " + refresh_token, "Content-Type": "application/json"}
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        return "Logged out"


def get_patients(access_token: str, refresh_token: str) -> [dict, str]:
    response, access_token = _send_request(requests.get, "/patient/",
                                           access_token=access_token,
                                           refresh_token=refresh_token)

    return response.json(), access_token


def logout(refresh_token: str):
    response = _send_request(requests.delete, "auth/logout", refresh_token=refresh_token)


def main():
    access_token, refresh_token = login()
    patients, access_token = get_patients(access_token, refresh_token)
    time.sleep(7)
    patients, access_token = get_patients(access_token, refresh_token)
    logout(refresh_token)


if __name__ == "__main__":
    main()
