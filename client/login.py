import json
import time
from datetime import datetime

import requests

BASE_URL = "http://localhost:5000/api/"
BASE_HEADER = {"Content-Type": "application/json"}


def _prepare_header(token):
    header = BASE_HEADER.copy()
    header["Authorization"] = f"Bearer {token}"
    return header


def login() -> [str, str]:
    login_data = {"username": "client", "password": "123456"}
    response = requests.post(BASE_URL + "auth/", data=json.dumps(login_data), headers=BASE_HEADER)
    return response


def refresh_login(refresh_token: str):
    response = requests.get(BASE_URL + "auth/", headers=_prepare_header(refresh_token))
    return response


def get_patients(access_token: str) -> [dict, str]:
    response = requests.get(BASE_URL + "patient/", headers=_prepare_header(access_token))
    return response


def update_patient(access_token: str, name) -> [dict, str]:
    data = {"name": name}
    response = requests.put(BASE_URL + "patient/1", data=json.dumps(data), headers=_prepare_header(access_token))
    return response


def delete_patient(access_token: str, id) -> [dict, str]:
    response = requests.delete(BASE_URL + "patient/" + str(id), headers=_prepare_header(access_token))
    return response


def add_patient(access_token: str) -> [dict, str]:
    date = datetime(1971, 7, 30).isoformat()
    data = {"name": "Hans", "surname": "Meier", "birthday": date}
    response = requests.post(BASE_URL + "patient/", data=json.dumps(data), headers=_prepare_header(access_token))
    return response


def logout(refresh_token: str):
    response = requests.delete(BASE_URL + "auth/", headers=_prepare_header(refresh_token))
    return response


def main():
    response = login()
    access_token = response.json()["access_token"]
    refresh_token = response.json()["refresh_token"]
    print(f"login: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = refresh_login(refresh_token)
    access_token = response.json()["access_token"]
    print(f"refresh: {response.json()}")

    response = update_patient(access_token, "Harald")
    print(f"update: {response.json()}")

    response = add_patient(access_token)

    patient_id = response.json()['id']
    print(f"add: {response.json()}")

    response = get_patients(access_token)
    print(f"patients: {response.json()}")

    response = delete_patient(access_token, patient_id)
    print(f"delete: {response.json()}")

    response = update_patient(access_token, "Luca")
    print(f"update: {response.json()}")

    response = logout(refresh_token)
    print(f"logout: {response.json()}")


if __name__ == "__main__":
    main()
