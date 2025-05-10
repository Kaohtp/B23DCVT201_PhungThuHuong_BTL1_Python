# Phân cụm cầu thủ dựa trên các chỉ số thống kê bằng thuật toán K-means và giảm chiều dữ liệu bằng PCA
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os
# Thêm đường dẫn đến file config
sys.path.append('SourceCode/Ex2')
import config as config

# Tạo thư mục xuất kết quả
OUTPUT_DIR = "Report/OUTPUT_BAI3"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def prepare_data():
    df = pd.read_csv(config.CSV_PATH, na_values=config.NA_VALUES)
    stats_columns = [col for col in df.columns if col not in config.IGNORE_STATS and col != config.TEAM_COLUMN]
    X = df[stats_columns].copy()
    X = X.fillna(X.mean())
    X = X.apply(pd.to_numeric, errors='coerce')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, df[config.TEAM_COLUMN], stats_columns

def find_optimal_clusters(X_scaled, max_clusters=10):
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X_scaled)
        inertias.append(kmeans.inertia_)
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, max_clusters + 1), inertias, 'bo-')
    plt.xlabel('Number of Clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.savefig(os.path.join(OUTPUT_DIR, 'elbow_plot.png'))
    plt.close()

def perform_clustering(X_scaled, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    return clusters, kmeans

def visualize_clusters(X_scaled, clusters, teams):
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    plot_df = pd.DataFrame({
        'PC1': X_pca[:, 0],
        'PC2': X_pca[:, 1],
        'Cluster': clusters,
        'Team': teams
    })
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=plot_df, x='PC1', y='PC2', hue='Cluster', palette='deep')
    plt.title('Player Clusters in 2D Space (PCA)')
    plt.savefig(os.path.join(OUTPUT_DIR, 'player_clusters.png'))
    plt.close()
    print("\nPrincipal Components Analysis Results:")
    print(f"Explained variance ratio: {pca.explained_variance_ratio_}")
    print(f"Total explained variance: {sum(pca.explained_variance_ratio_):.2%}")

def analyze_clusters(df, clusters, stats_columns):
    df['Cluster'] = clusters
    df.to_csv(os.path.join(OUTPUT_DIR, "clustered_players.csv"), index=False)
    print("\nCluster Analysis:")
    for cluster in range(max(clusters) + 1):
        cluster_data = df[df['Cluster'] == cluster]
        print(f"\nCluster {cluster} ({len(cluster_data)} players):")
        print(f"Teams in cluster: {', '.join(cluster_data[config.TEAM_COLUMN].unique())}")
        cluster_means = cluster_data[stats_columns].mean()
        print("\nTop 5 highest average statistics:")
        print(cluster_means.nlargest(5))
        cluster_data.to_csv(os.path.join(OUTPUT_DIR, f"cluster_{cluster}_players.csv"), index=False)

def main():
    X_scaled, teams, stats_columns = prepare_data()
    find_optimal_clusters(X_scaled)
    n_clusters = 6
    clusters, kmeans = perform_clustering(X_scaled, n_clusters)
    visualize_clusters(X_scaled, clusters, teams)
    df = pd.read_csv(config.CSV_PATH, na_values=config.NA_VALUES)
    analyze_clusters(df, clusters, stats_columns)

if __name__ == "__main__":
    main()
