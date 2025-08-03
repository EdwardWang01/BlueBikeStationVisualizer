import os
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import geopandas as gpd
import contextily as cx
from shapely.geometry import Point

# Folder where your snapshots are stored, replace with your own path
DATA_FOLDER = "C:/Users/edwan/Downloads/bluebike_data"


# List to store rows of processed data
rows = []

# Loop over all JSON files in the folder
for filename in sorted(os.listdir(DATA_FOLDER)):
    if filename.endswith(".json"):
        timestamp_str = filename.replace(".json", "")
        try:
            # Convert filename timestamp to datetime object
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d_%H-%M-%S")
        except ValueError:
            print(f"Skipping file with invalid timestamp format: {filename}")
            continue

        filepath = os.path.join(DATA_FOLDER, filename)
        with open(filepath, "r") as f:
            data = json.load(f)

        stations = data["data"]["stations"]
        for station in stations:
            station_id = station["station_id"]
            num_bikes = station["num_bikes_available"]
            rows.append({
                "station_id": station_id,
                "timestamp": timestamp,
                "num_bikes_available": num_bikes
            })

# Create a DataFrame
df = pd.DataFrame(rows)

# merge station_status_over_time.csv with station_information.json

with open("station_information.json", "r") as f:
    info = json.load(f)

station_rows = []
for station in info["data"]["stations"]:
    station_rows.append({
        "station_id": station["station_id"],
        "name": station["name"],
        "lat": station["lat"],
        "lon": station["lon"],
        "capacity": station["capacity"]
    })

# Convert to DataFrame
info_df = pd.DataFrame(station_rows)

# Merge on station_id
merged_df = pd.merge(df, info_df, on="station_id", how="left")

# Save the merged data
merged_df.to_csv("station_status_with_locations.csv", index=False)
print("✅ Saved merged file: station_status_with_locations.csv")

# Filter out stations with missing capacity to avoid divide-by-zero
merged_df = merged_df.dropna(subset=["capacity"])
merged_df = merged_df[merged_df["capacity"] > 0]

# Compute fullness (0 = empty, 1 = full)
merged_df["fullness"] = merged_df["num_bikes_available"] / merged_df["capacity"]
merged_df["fullness"] = merged_df["fullness"].clip(0, 1)

#animation time

# Helper: convert each frame to GeoDataFrame
def get_frame_gdf(frame_data):
    geometry = [Point(xy) for xy in zip(frame_data["lon"], frame_data["lat"])]
    gdf = gpd.GeoDataFrame(frame_data, geometry=geometry, crs="EPSG:4326")
    return gdf.to_crs(epsg=3857)

# Initial data
timestamps = sorted(merged_df["timestamp"].unique())
frame_data = merged_df[merged_df["timestamp"] == timestamps[0]]
gdf = get_frame_gdf(frame_data)

# Plot setup
fig, ax = plt.subplots(figsize=(12, 12))
scat = ax.scatter(
    gdf.geometry.x, gdf.geometry.y,
    s=40,  # fixed dot size
    c=frame_data["fullness"],
    cmap="RdYlGn",
    vmin=0, vmax=1,
    alpha=0.8,
    edgecolor="k"
)

cx.add_basemap(ax, source=cx.providers.CartoDB.Positron)
ax.set_axis_off()

# Update function
def update(frame):
    current_time = timestamps[frame]
    frame_data = merged_df[merged_df["timestamp"] == current_time]
    gdf = get_frame_gdf(frame_data)

    scat.set_offsets(list(zip(gdf.geometry.x, gdf.geometry.y)))
    scat.set_array(frame_data["fullness"])
    ax.set_title(f"Bluebike Station Fullness – {current_time}", fontsize=16)

    return scat,

# Animate
ani = FuncAnimation(fig, update, frames=len(timestamps), interval=300)
plt.tight_layout()
plt.show()