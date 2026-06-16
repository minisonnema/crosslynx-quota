from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(__name__)

ACCESS_TOKEN = "ddbcceb39f4555d4cda517560c117f93"
ORGANIZATION_ID = "pXPgma"
GROUP_ID = "35"

BASE_URL = "https://api.ic.peplink.com/rest"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/api/quota')
def get_quota():
    try:
        # Meest waarschijnlijke endpoints voor Guest Account
        endpoints = [
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal/guest_accounts",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/guest_accounts",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info/csv"
        ]
        
        for url in endpoints:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                    if isinstance(data, list):
                        users = []
                        for item in data:
                            users.append({
                                "name": item.get("username") or item.get("name", "Onbekend"),
                                "quota": item.get("quota") or item.get("data_usage_quota", "N/A"),
                                "used": item.get("used") or "0 GB",
                                "remaining": item.get("remaining") or item.get("quota_left", "N/A")
                            })
                        return jsonify(users)
                except:
                    pass
                
                # Als het CSV is
                if "," in resp.text:
                    users = []
                    lines = resp.text.strip().split("\n")
                    for line in lines[1:]:
                        if line.strip():
                            fields = [f.strip() for f in line.split(",")]
                            if len(fields) >= 1:
                                users.append({
                                    "name": fields[0],
                                    "quota": fields[1] if len(fields) > 1 else "N/A",
                                    "used": fields[2] if len(fields) > 2 else "0 GB",
                                    "remaining": fields[1] if len(fields) > 1 else "N/A"
                                })
                    return jsonify(users)
        
        return jsonify({"error": "Geen geldige data gevonden", "tried": len(endpoints)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/quota.html')
def quota_page():
    return send_from_directory('.', 'quota.html')

@app.route('/')
def index():
    return "<h1>Quota Overzicht</h1><p><a href='/quota.html'>→ Ga naar Quota Overzicht</a></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
