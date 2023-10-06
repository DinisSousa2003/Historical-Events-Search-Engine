import folium
from shapely import wkt
from collections import defaultdict
from sklearn.cluster import DBSCAN
import numpy as np
from branca.colormap import LinearColormap
import json

# Read your JSON file and extract the coordinates
# Replace 'your_data.json' with the path to your JSON file
with open('outputs/data.json', 'r') as json_file:
    data = json.load(json_file)

# Extract and store the coordinates
coordinates = []

for entry in data:
    if "coordinate location" in entry:
        coordinate_location = entry["coordinate location"]
        point = wkt.loads(coordinate_location)

        if hasattr(point, 'geom_type') and point.geom_type == "Point":
            latitude, longitude = point.x, point.y
            coordinates.append([latitude, longitude])

# Convert the list of coordinates to a NumPy array for DBSCAN
coordinates = np.array(coordinates)

# Create a DBSCAN model to cluster the coordinates
eps = 0.1  # Adjust this value to control the clustering radius
min_samples = 1  # Adjust this value based on your data
dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(coordinates)

# Calculate the center of Europe based on your data or approximate coordinates
# For example, you can use the coordinates of a central European city like Vienna, Austria:
europe_center = [48.2082, 16.3738]

# Create a folium map centered on Europe
m = folium.Map(location=europe_center, zoom_start=5)  # Adjust the zoom level as needed

# Create a dictionary to store cluster points and their counts
cluster_counts = defaultdict(int)

# Iterate through the clusters and count points in each cluster
for i, label in enumerate(dbscan.labels_):
    if label != -1:  # Ignore noise points (label=-1)
        latitude, longitude = coordinates[i]

        # Increase the count for this cluster
        cluster_counts[label] += 1

# Define a colormap based on the count of points in clusters
colormap = LinearColormap(colors=['blue', 'red'], vmin=min(cluster_counts.values()), vmax=max(cluster_counts.values()))

# Iterate through the clusters and add them to the map with colored circle markers
for label, count in cluster_counts.items():
    # Find the coordinates in the cluster
    cluster_indices = np.where(dbscan.labels_ == label)[0]
    cluster_coordinates = coordinates[cluster_indices]

    # Calculate the cluster center (mean of coordinates)
    cluster_center = np.mean(cluster_coordinates, axis=0)

    # Create a Marker for each cluster center with a popup displaying the count
    folium.CircleMarker(
        location=cluster_center[::-1],  # Reverse the order of coordinates
        radius=2* count,  # Adjust the radius based on the count
        popup=f'Count: {count}',
        fill=True,
        color=colormap(count),
        fill_opacity=0.6
    ).add_to(m)

# Add the colormap to the map
colormap.caption = 'Cluster Size'
colormap.add_to(m)

# Save the map to an HTML file or display it in a Jupyter Notebook
m.save('map.html')
