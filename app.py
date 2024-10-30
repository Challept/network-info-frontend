from flask import Flask, jsonify
from flask_cors import CORS
import socket
import subprocess
import platform

app = Flask(__name__)
CORS(app)  # Aktivera CORS-stöd

def get_network_info():
    ssid = "Unknown Network"
    password = "Unavailable"
    if platform.system() == "Windows":
        try:
            # Hämta SSID
            result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "SSID" in line and "BSSID" not in line:  # Undvik linjer med "BSSID"
                    ssid = line.split(":")[1].strip()
                    break
            # Hämta lösenord
            result = subprocess.run(["netsh", "wlan", "show", "profile", ssid, "key=clear"], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if "Key Content" in line:
                    password = line.split(":")[1].strip()
                    break
        except Exception as e:
            print("Could not retrieve network info:", e)
    else:
        print("Platform not supported for network info retrieval")
    return ssid, password

def get_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except Exception as e:
        print("Could not retrieve IP address:", e)
        return "Unavailable"

@app.route('/api/network_info', methods=['GET'])
def network_info():
    ssid, password = get_network_info()
    ip_address = get_ip()
    return jsonify({
        'ssid': ssid,
        'password': password,
        'ip_address': ip_address
    })

if __name__ == '__main__':
    print("Starting Flask server on http://0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000)