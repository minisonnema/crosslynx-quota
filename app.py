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
        
        raw = response.text.strip()
        
        return jsonify({
            "status": response.status_code,
            "users_found": 0,
            "raw_data": raw[:1500],   # eerste 1500 tekens voor debug
            "message": "Geen gebruikers gevonden of lege response"
        })
    
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
