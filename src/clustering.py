import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# The function below selects training columns from the song feature dataset,
# splits the data into train/test, and fits a KMeans model with the best silhouette score
def run_clustering_model(df):
    # Select columns useful for training
    train_column = ['num_samples', 'duration', 'end_of_fade_in', 'start_of_fade_out',
                    'loudness', 'tempo', 'tempo_confidence', 'time_signature',
                    'time_signature_confidence', 'key', 'key_confidence', 'mode',
                    'mode_confidence', 'danceability', 'energy', 'speechiness',
                    'acousticness', 'instrumentalness', 'liveness', 'valence',
                    'duration_ms']

    # Split into training and test sets
    X_train, X_test = train_test_split(df, test_size=0.1)

    # Silhouette score loop to help find best number of clusters
    silhouette_scores = []
    for k in range(400, 550):
        clus = KMeans(n_clusters=k, random_state=42)
        clus.fit(X_train[train_column])
        score = silhouette_score(X_train[train_column], clus.labels_)
        silhouette_scores.append(score)

    # Plot the scores (optional)
    plt.plot(range(400, 550), silhouette_scores)
    plt.grid(True)
    plt.xlabel("Number of Clusters")
    plt.ylabel("Silhouette Score")
    plt.title("KMeans Clustering Evaluation")
    plt.show()

    # Print more focused range
    for k in range(440, 450):
        clus = KMeans(n_clusters=k, random_state=42)
        clus.fit(X_train[train_column])
        score = silhouette_score(X_train[train_column], clus.labels_)
        print(f"silhouette_score: {score:.4f} | number of clusters: {k}")

    # Final model using selected number of clusters
    kmeans = KMeans(n_clusters=443, random_state=42)
    kmeans.fit(X_train[train_column])

    return kmeans, X_train, train_column
