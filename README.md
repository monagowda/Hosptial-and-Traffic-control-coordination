# Ambulance Emergency Simulation

A simple offline simulation of an ambulance sending live GPS updates to a hospital and traffic police, so they can track its location and ETA in real time.

## How It Works

1. **`broker.py`** — A local message hub. It runs on `127.0.0.1:5555` and relays messages between the ambulance and the responders (hospital + traffic police).
2. **`ambulance.py`** — Simulates an ambulance driving along a fixed route. It sends GPS position, ETA, and status updates every few seconds.
3. **`responders.py`** — Listens for updates from the broker and generates a live map dashboard (using Folium/Leaflet) for both the hospital and traffic police.
4. **`hospital_dashboard.html`** / **`traffic_police_dashboard.html`** — Auto-generated map files showing the ambulance's route, current position, and destination. These update automatically each time new GPS data arrives.

## Running the Simulation

Open three terminals and run these in order:

```bash
# Terminal 1 - start the hub
python broker.py

# Terminal 2 - start the responders (hospital + traffic police)
python responders.py

# Terminal 3 - start the ambulance
python ambulance.py
```

As the ambulance "moves," `responders.py` will regenerate `hospital_dashboard.html` and `traffic_police_dashboard.html`. Open either file in a browser and refresh it to see the ambulance's updated position on the map.

## Notes

- Everything runs locally on `127.0.0.1` — no internet connection is required except for loading map tiles and libraries in the HTML dashboards.
- The route and ETA values in `ambulance.py` are hardcoded for demo purposes; you can edit `simulated_route` to try different paths.
