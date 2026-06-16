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
        url = f"{BASE_URL}/o/{ORGANIZATION_ID}/g/{GROUP_ID}/captive_portal_user_info_csv"
        
        response = requests.get(url, headers=headers, timeout=15)
        
        # Debug informatie
        debug = {
            "status_code": response.status_code,
            "raw_response": response.text[:1000] if response.text else "Lege response",
            "headers": dict(response.headers)
        }
        
        if response.status_code != 200:
            return jsonify({"error": f"API fout: {response.status_code}", "debug": debug}), 500

        # Probeer data te parsen
        users = []
        lines = response.text.strip().split("\n")
        
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

        return jsonify({"users": users, "debug": debug})
    
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
