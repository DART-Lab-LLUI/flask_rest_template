import requests

response = requests.post(
    'http://localhost:5000/api/auth/',
    headers={"Content-Type": "application/json"},
    json={"username": "both", "password": "1234"}
)

# View the new `text-matches` array which provides information
# about your search term within the results
print(response.status_code)
json_response = response.json()
print(json_response)

response = requests.get(
    'http://localhost:5000/api/patient/',
    headers={"Authorization": "Bearer " + json_response["access_token"], "Content-Type": "application/json"}
)

print(response.status_code)
