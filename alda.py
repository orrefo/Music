import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("all.csv")
    return data

data = load_data()

# Preprocess data: Group by artist to calculate the total points 
artist_scores = data.groupby("artist", as_index=False)["score"].sum()


# Sidebar Navigation
st.sidebar.title("🎵 Dashboard Navigation")
section = st.sidebar.radio(
    "Select a Section",
    [
        "🎤 Artist Insights",
        "⚔️ Artist Duel: Who’s the Star?"
    ]
)

# Section 1: Artist Insights
if section == "🎤 Artist Insights":
    st.title("🎤 Artist Insights")
    st.write(
        "Discover the top artists based on popularity and explore their metrics with customizable filters."
    )

    # Filters
    popularity_threshold = st.slider(
        "Minimum Popularity", 0, 100, 50, 
        help="Adjust to filter artists by their popularity score."
    )
    explicit_filter = st.checkbox(
        "Include Explicit Artists", 
        value=True, 
        help="Toggle to include or exclude explicit artists."
    )

    # Group data by artist to make artists unique
    grouped_artists = data.groupby("artist", as_index=False).agg({
        "popularity": "mean",  # Average popularity score
        "followers": "sum",    # Total followers for each artist
        "explicit": "any"      # Check if any track is explicit
    })

    # Apply filters dynamically
    filtered_artists = grouped_artists[grouped_artists['popularity'] >= popularity_threshold]
    if not explicit_filter:
        filtered_artists = filtered_artists[~filtered_artists['explicit']]

    # Sort by popularity (descending order)
    filtered_artists = filtered_artists.sort_values("popularity", ascending=False)

    # Top Artists Visualization (Dynamic)
    st.subheader("🎵 Top Artists Chart")
    fig = px.bar(
        filtered_artists.head(10),  # Show top 10 artists
        x="artist",
        y="popularity",
        title="🎵 Top 10 Artists by Popularity",
        color="explicit",
        labels={"artist": "Artist", "popularity": "Popularity"},
        color_discrete_map={True: "#FF6347", False: "#4682B4"},
        template="plotly_white",
        hover_data={"popularity": True, "followers": True, "explicit": True}
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Dynamic Filtered Artists Table
    st.subheader("🎧 Filtered Artists Data")
    st.dataframe(
        filtered_artists[["artist", "popularity", "followers", "explicit"]], 
        use_container_width=True
    )
    # Score Growth Over Time
    st.subheader("📈 Artist Score Growth Over Time")
    artist_choice = st.selectbox("Select an Artist", data["artist"].unique())
    artist_data = data[data["artist"] == artist_choice]

    if not artist_data.empty:
        fig = px.line(
            artist_data.sort_values("chart_year"),
            x="chart_year",
            y="score",
            title=f"Score Growth for {artist_choice}",
            labels={"chart_year": "Chart Year", "score": "Score"},
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No data available for the selected artist.")


# Section 2: Artist Duel
elif section == "⚔️ Artist Duel: Who’s the Star?":
    st.title("⚔️ Artist Duel: Who’s the Star?")
    st.write(
        "Compare two artists head-to-head on various metrics like popularity, followers, and energy."
    )
    
    # Select Artists
    artist_1 = st.selectbox("Choose Artist 1", artist_scores["artist"].unique())
    artist_2 = st.selectbox("Choose Artist 2", artist_scores["artist"].unique())
    artist_1_data = data[data["artist"] == artist_1]
    artist_2_data = data[data["artist"] == artist_2]
    
    # Get overall scores for each artist
    artist_1_score = artist_scores[artist_scores["artist"] == artist_1]["score"].values[0]
    artist_2_score = artist_scores[artist_scores["artist"] == artist_2]["score"].values[0]

    # Display overall scores as a bar chart
    st.subheader("🌟 Overall Points Comparison")
    overall_score_data = pd.DataFrame({
        "Artist": [artist_1, artist_2],
        "Score": [artist_1_score, artist_2_score]
    })
    fig = px.bar(
        overall_score_data,
        x="Artist",
        y="Score",
        title="🌟 Overall Score Comparison",
        labels={"Artist": "Artist", "Score": "Overall Score"},
        color="Artist",
        color_discrete_sequence=["#85c1e9", "#f0b27a"],
        template="plotly_white"
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Artist Duel Comparison Metrics
    metrics = {
        "🎶 Popularity": "popularity",
        "👥 Followers": "followers",
        "💃 Danceability": "danceability",
        "⚡ Energy": "energy",
        "🎭 Valence (Mood)": "valence",
        "🎵 Tempo": "tempo"
    }

    # Loop through each metric to create individual charts
    for metric_name, metric_column in metrics.items():
        st.subheader(f"{metric_name}")
        
        # Calculate averages for each artist
        duel_data = pd.DataFrame({
            "Artist": [artist_1, artist_2],
            "Score": [
                artist_1_data[metric_column].mean(),
                artist_2_data[metric_column].mean()
            ]
        })
        
        # Create bar chart for the metric
        fig = px.bar(
            duel_data,
            x="Artist",
            y="Score",
            title=f"{metric_name}: {artist_1} vs {artist_2}",
            labels={"Artist": "Artist", "Score": metric_name},
            color="Artist",
            color_discrete_sequence=["#85c1e9", "#f0b27a"],
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

    # Display Summary Table
    st.subheader("📊 Summary of Comparison Metrics")

    # Create the summary DataFrame
    summary_data = pd.DataFrame({
        "Metric": ["🌟 Overall Score"] + list(metrics.keys()),
        artist_1: [artist_1_score] + [artist_1_data[col].mean() for col in metrics.values()],
        artist_2: [artist_2_score] + [artist_2_data[col].mean() for col in metrics.values()],
    })


    # Displaying
    st.dataframe(summary_data, use_container_width=True)
