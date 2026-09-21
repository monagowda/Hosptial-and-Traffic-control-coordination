import time
import json
import socket

HOST = '127.0.0.1'
PORT = 5555

# Simulated GPS Route coordinates (From Incident Site to Hospital)
simulated_route = [
    [12.9716, 77.5946],  
    [12.9750, 77.5990],  
    [12.9790, 77.6040],  
    [12.9830, 77.6090],  
    [12.9870, 77.6140]   
]

print("🚑 AMBULANCE TRANSMITTER ONLINE")
print("Connecting to local simulation hub...")

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("✅ Connected successfully!\n")

    for index, coords in enumerate(simulated_route):
        payload = {
            "ambulance_id": "AMB-ZONE-4",
            "current_position": coords,
            "full_route": simulated_route,
            "eta_minutes": 12 - (index * 2),
            "status": "CRITICAL_PATIENT"
        }
        
        # Send data across the local socket
        client.send(json.dumps(payload).encode('utf-8'))
        print(f"📡 GPS Ping Sent: {coords} | ETA: {payload['eta_minutes']} Mins.")
        
        time.sleep(4) # 4 seconds between movements
        
    print("\n🏁 Destination Reached. Patient Admitted.")
except Exception as e:
    print(f"❌ Connection Error: {e}")
finally:
    client.close()