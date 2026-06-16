from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(__name__)

ACCESS_TOKEN = "581985d14120b829df624ebcc1d2d63c"
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
        # Meest waarschijnlijke endpoints
        urls = [
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info/csv",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info_csv",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal/users"
        ]
        
        for url in urls:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                break
            print(f"Probeerde {url} → {response.status_code}")
        
        if response.status_code != 200:
            return jsonify({
                "error": f"Peplink API fout: {response.status_code}",
                "details": response.text
            }), 500

        # ... (rest van de code blijft hetzelfde)
        users = []
        lines = response.text.strip().split("\n")
        for line in lines[1:]:
            if line.strip():
                fields = [f.strip() for f in line.split(",")]
                if len(fields) >= 2:
                    username = fields[0]
                    quota = fields[1] if len(fields) > 1 else "N/A"
                    used = fields[2] if len(fields) > 2 else "0 GB"
                    users.append({
                        "name": username,
                        "quota": quota,
                        "used": used,
                        "remaining": quota
                    })
        
        return jsonify(users)
    
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
