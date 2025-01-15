import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt

# Load the dataset (update the path if needed)
file_path = "c:/Users/fberg/orrefo(music)/Music/all.csv"  # Replace with your file's path
audio_data = pd.read_csv(file_path)

# Select relevant audio features
audio_features = audio_data[
    ['danceability', 'energy', 'loudness', 'speechiness',
     'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo']
]

# Drop rows with missing values
cleaned_audio_features = audio_features.dropna()

# Scale the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(cleaned_audio_features)

# Determine the optimal number of clusters using the elbow method and silhouette analysis
inertia = []  # For the Elbow Method
silhouette_scores = []  # For Silhouette Scores
k_range = range(2, 11)  # Test cluster sizes from 2 to 10

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_features)
    inertia.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(scaled_features, kmeans.labels_))

# Plot the results
plt.figure(figsize=(12, 5))

# Elbow Method Plot
plt.subplot(1, 2, 1)
plt.plot(k_range, inertia, marker='o', label='Inertia')
plt.title('Elbow Method')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.xticks(k_range)
plt.legend()

# Silhouette Score Plot
plt.subplot(1, 2, 2)
plt.plot(k_range, silhouette_scores, marker='o', color='orange', label='Silhouette Score')
plt.title('Silhouette Scores')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Silhouette Score')
plt.xticks(k_range)
plt.legend()

plt.tight_layout()
plt.show()
