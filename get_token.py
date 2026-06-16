import requests

client_id = "PLAK_HIER_CLIENT_ID"
client_secret = "PLAK_HIER_CLIENT_SECRET"

url = "https://api.ic.peplink.com/api/oauth2/token"

data = {
    "client_id": 30bdfcb975362cf23aee7d11568278c9,
    "client_secret": 581985d14120b829df624ebcc1d2d63c,
    "grant_type": "client_credentials"
}

response = requests.post(url, data=data)

if response.status_code == 200:
    token = response.json()["access_token"]
    print("✅ SUCCESS! Je Access Token is:")
    print(token)
    print("\nKopieer deze token en gebruik hem in app.py")
else:
    print("Fout:", response.status_code)
    print(response.text)
