import json
import socket
import folium

HOST = '127.0.0.1'
PORT = 5555

def generate_interactive_map(data, user_type):
    curr_pos = data["current_position"]
    route = data["full_route"]
    
    mymap = folium.Map(location=curr_pos, zoom_start=14)
    folium.PolyLine(route, color="red", weight=6, opacity=0.7, tooltip="Ambulance Path").add_to(mymap)
    
    # Custom markers
    folium.Marker(location=curr_pos, popup=f"Ambulance\nETA: {data['eta_minutes']}m", icon=folium.Icon(color="red", icon="ambulance", prefix="fa")).add_to(mymap)
    folium.Marker(location=route[-1], popup="Destination Hospital", icon=folium.Icon(color="green", icon="hospital-o", prefix="fa")).add_to(mymap)

    filename = f"{user_type}_dashboard.html"
    mymap.save(filename)
    print(f"🗺️ Map Graphic updated for {user_type.upper()} ({filename})")

def start_responder():
    print("🖥️  CONTROL ROOM SYSTEM ONLINE")
    print("Connecting to local simulation hub...")
    
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print("✅ Connected and listening for emergency broadcasts...\n")
        
        while True:
            message = client.recv(4096).decode('utf-8')
            if not message:
                break
                
            data = json.loads(message)
            print(f"\n🚨 [INCOMING ALERT] {data['ambulance_id']} is active!")
            
            # 1. Hospital Pipeline
            print(f"🏥 [HOSPITAL ER]: Preparing trauma bed. ETA: {data['eta_minutes']} mins.")
            generate_interactive_map(data, "hospital")
            
            # 2. Traffic Police Pipeline
            print(f"👮 [TRAFFIC POLICE]: Clearing path ahead at: {data['current_position']}.")
            generate_interactive_map(data, "traffic_police")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_responder()
