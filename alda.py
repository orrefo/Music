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
data["chart_week"] = pd.to_datetime(data["chart_week"], errors="coerce")

# Section 1: Artist Insights
if section == "🎤 Artist Insights":
    st.title("🎤 Artist Insights")
    
    # 1. Artist Filter
    st.subheader("Filter by Artist")
    artist_choice = st.selectbox("Select an Artist", data["artist"].unique())
    artist_data = data[data["artist"] == artist_choice]

    # Ensure data exists for the selected artist
    if artist_data.empty:
        st.write("No data available for the selected artist.")
    else:
        # 2. Artist Score Growth Over Time
        st.subheader("📈 Artist Score Growth Over Time")

        # Group by year dynamically
        artist_data_yearly = (
            artist_data.groupby(artist_data["chart_week"].dt.year)
            .agg({"score": "sum"})
            .reset_index()
            .rename(columns={"chart_week": "Year"})
        )

        # Ensure the Year column is an integer
        artist_data_yearly["Year"] = artist_data_yearly["Year"].astype(int)

        # Allow user to select a range of years
        min_year, max_year = artist_data_yearly["Year"].min(), artist_data_yearly["Year"].max()
        selected_years = st.slider(
            "Select Year Range",
            min_value=min_year,
            max_value=max_year,
            value=(min_year, max_year),
            step=1,
            help="Drag the slider to filter data by year range."
        )

        # Filter the data based on the selected year range
        filtered_data = artist_data_yearly[
            (artist_data_yearly["Year"] >= selected_years[0]) &
            (artist_data_yearly["Year"] <= selected_years[1])
        ]

        # Create the line chart
        fig = px.line(
            filtered_data,
            x="Year",
            y="score",
            title=f"Score Growth for {artist_choice} ({selected_years[0]} - {selected_years[1]})",
            labels={"Year": "Year", "score": "Score"},
            template="plotly_white"
        )
        fig.update_layout(title_x=0.5)
        st.plotly_chart(fig, use_container_width=True)

        # 3. Most Successful Tracks by Chart Appearances
        st.subheader("Most Successful Tracks by Chart Appearances")
        track_success_count = (
            artist_data.groupby(["track_title", "artist"], as_index=False)
            .agg({"list_position": "count", "release_date": "min"})  # Count chart appearances and get earliest release date
            .rename(columns={"list_position": "num_chart_appearances"})  # Rename column for clarity
            .sort_values("num_chart_appearances", ascending=False)  # Sort by the number of appearances
        )

        top_successful_tracks = track_success_count.head(5)
        st.write(top_successful_tracks[["track_title", "num_chart_appearances", "release_date"]])

        fig = px.bar(
            top_successful_tracks,
            x="track_title",
            y="num_chart_appearances",
            title=f"Most Successful Tracks for {artist_choice}",
            labels={"track_title": "Track Title", "num_chart_appearances": "Chart Appearances"},
            text="num_chart_appearances",  # Display chart appearances count on bars
        )
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(title_x=0.5, template="plotly_white", height=600, width=1000,)
        st.plotly_chart(fig, use_container_width=True)

        # 4. Track Type Distribution
        st.subheader(f"Track Type Distribution for {artist_choice}")
        unique_tracks = artist_data.groupby("track_id", as_index=False).first()  # Ensure unique tracks by grouping on track_id
        track_types = unique_tracks["album_type"].value_counts().reset_index()
        track_types.columns = ["album_type", "count"]

        fig = px.pie(
            track_types,
            values="count",
            names="album_type",
            title=f"Album Type Distribution for {artist_choice}",
            labels={"album_type": "Album Type", "count": "Count"},
            template="plotly_white"
        )
        st.plotly_chart(fig)

    # 5. Discover Top Artists
    
    st.subheader("Discover the Top Artists")
    st.write("Explore the top artists based on popularity and customize filters to refine the view.")

    # Range slider for popularity
    popularity_range = st.slider(
        "Select Popularity Range",
        min_value=int(data["popularity"].min()),
        max_value=int(data["popularity"].max()),
        value=(50, 100),  # Default range
        step=1,
        help="Select the range of popularity scores to filter artists."
    )

    explicit_filter = st.checkbox(
        "Include Explicit Artists",
        value=True,
        help="Toggle to include or exclude explicit artists."
    )

    # Group data by artist
    grouped_artists = data.groupby("artist", as_index=False).agg({
        "popularity": "mean",  # Average popularity score
        "followers": "sum",    # Total followers for each artist
        "explicit": "any",     # Check if any track is explicit
        "score": "sum"         # Total score for the artist
    })

    # Apply filters
    filtered_artists = grouped_artists[
        (grouped_artists['popularity'] >= popularity_range[0]) &
        (grouped_artists['popularity'] <= popularity_range[1])
    ]
    if not explicit_filter:
        filtered_artists = filtered_artists[~filtered_artists['explicit']]

    # Sort by popularity
    filtered_artists = filtered_artists.sort_values("popularity", ascending=False)

    # Top Artists Chart
    fig = px.bar(
        filtered_artists.head(10),
        x="artist",
        y="popularity",
        title="Top 10 Artists by Popularity",
        color="explicit",
        labels={"artist": "Artist", "popularity": "Popularity"},
        color_discrete_map={True: "#FF6347", False: "#4682B4"},
        template="plotly_white",
        hover_data={"popularity": True, "followers": True, "explicit": True}
    )
    fig.update_layout(title_x=0.5)
    st.plotly_chart(fig, use_container_width=True)

    # Filtered Artists Data Table
    st.subheader("Filtered Artists Data")
    st.dataframe(filtered_artists[["artist", "popularity", "followers", "explicit", "score"]], use_container_width=True)




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
        "🎭 Valence (Mood)": "valence"
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
