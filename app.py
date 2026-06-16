from flask import Flask, jsonify, send_from_directory
import requests

app = Flask(__name__)

# ================== CONFIGURATIE ==================
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
        # Officiële endpoints uit Peplink API docs
        endpoints = [
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info",
            f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info/csv"
        ]
        
        response = None
        used_url = ""
        
        for url in endpoints:
            resp = requests.get(url, headers=headers, timeout=15)
            used_url = url
            if resp.status_code == 200:
                response = resp
                break
        
        if not response or response.status_code != 200:
            return jsonify({
                "error": f"API fout: {response.status_code if response else 'No response'}",
                "details": f"Probeerde: {used_url}\n{response.text if response else 'Geen response'}"
            }), 500

        # Verwerk data
        users = []
        raw = response.text.strip()
        
        if raw.startswith('['):  # JSON
            data = response.json()
            for item in data if isinstance(data, list) else []:
                users.append({
                    "name": item.get("username") or item.get("name", "Onbekend"),
                    "quota": item.get("quota", "N/A"),
                    "used": item.get("used", "0 GB"),
                    "remaining": item.get("remaining", "N/A")
                })
        else:  # CSV
            lines = raw.split("\n")
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
