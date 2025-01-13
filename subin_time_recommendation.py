import streamlit as st
import pandas as pd
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("all.csv")  # Replace with your file path
    return data

data = load_data()
data_track=data.groupby(['track_title','artist']).mean(numeric_only=True)



# Sidebar Navigation
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Artist Insights",
        "Track Insights",
        "Festival Lineup Optimizer",
        "Audio Feature Trends",
        "Build-Your-Own Playlist",
        "Nostalgia Mode: Hits from the Past",
        "Audience Participation Predictor",
        "Artist Duel: Who’s the Star?",
        "Audio Feature Mashup"
    ]
)

# Section 1: Artist Insights
if section == "Artist Insights":
    st.title("Artist Insights")
    st.subheader("Top Artists by Popularity")

    # Filters
    popularity_threshold = st.slider("Minimum Popularity", 0, 100, 50)
    explicit_filter = st.checkbox("Include Explicit Artists", value=True)

    # Filter the data
    filtered_artists = data[data['popularity'] >= popularity_threshold]
    if not explicit_filter:
        filtered_artists = filtered_artists[~filtered_artists['explicit']]

    # Top Artists Visualization
    fig = px.bar(
        filtered_artists.sort_values('popularity', ascending=False).head(10),
        x="artist",
        y="popularity",
        title="Top 10 Artists by Popularity",
        color="explicit",
        labels={"artist": "Artist", "popularity": "Popularity"},
        color_discrete_map={True: "red", False: "blue"}
    )
    st.plotly_chart(fig)

    # Display filtered data
    st.write(filtered_artists[["artist", "popularity", "followers", "explicit"]])

# Section 2: Track Insights
elif section == "Track Insights":
    st.title("Track Insights")
    st.subheader("Top Tracks by Year")

    # Filters
    year_filter = st.slider("Select Release Year", int(data["release_year"].min()), int(data["release_year"].max()), 2020)
    top_tracks = data[data["release_year"] == year_filter].sort_values("list_position").head(10)

    # Top Tracks Visualization
    fig = px.bar(
        top_tracks,
        x="track_title",
        y="list_position",
        title=f"Top 10 Tracks of {year_filter}",
        labels={"track_title": "Track Title", "list_position": "Chart Position"},
        color="explicit",
        color_discrete_map={True: "red", False: "blue"}
    )
    st.plotly_chart(fig)

    # Display Top Tracks Data
    st.write(top_tracks[["track_title", "artist", "list_position", "release_year", "explicit"]])

# Section 3: Festival Lineup Optimizer
elif section == "Festival Lineup Optimizer":
    st.title("Festival Lineup Optimizer")
    st.subheader("Mood Mapping")

    # Scatterplot for mood mapping
    fig = px.scatter(
        data,
        x="valence",
        y="energy",
        hover_data=["artist", "track_title"],
        title="Mood Mapping: Valence vs Energy",
        labels={"valence": "Valence (Positivity)", "energy": "Energy"},
        color="energy",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig)

    # Set Time Recommendations add the bpm
    st.subheader("Set Time Recommendations")
    time_of_day = st.radio("Select Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
    if time_of_day == "Morning":
        filtered_lineup = data_track[data_track["energy"] <= 0.4]
    elif time_of_day == "Afternoon":
        filtered_lineup = data_track[(data_track["energy"] > 0.4) & (data_track["energy"] <= 0.6)]
    elif time_of_day == "Evening":
        filtered_lineup = data_track[(data_track["energy"] > 0.6) & (data_track["energy"] <= 0.8)]
    else:
        filtered_lineup = data_track[data_track["energy"] > 0.8]

    st.write(f"Recommended Artists and Tracks for {time_of_day}")
    st.write(filtered_lineup[["artist", "track_title", "energy", "valence"]])

# Section 4: Audio Feature Trends
elif section == "Audio Feature Trends":
    st.title("Audio Feature Trends")
    feature = st.selectbox(
        "Select Audio Feature",
        ["danceability", "energy", "tempo", "valence", "acousticness", "loudness"]
    )
    feature_trends = data.groupby("release_year")[feature].mean().reset_index()
    fig = px.line(
        feature_trends,
        x="release_year",
        y=feature,
        title=f"{feature.capitalize()} Trends Over the Years",
        labels={"release_year": "Release Year", feature: feature.capitalize()}
    )
    st.plotly_chart(fig)

    st.subheader(f"{feature.capitalize()} Distribution")
    fig = px.histogram(data, x=feature, nbins=100, title=f"{feature.capitalize()} Distribution")
    st.plotly_chart(fig)

# Section 5: Build-Your-Own Playlist
elif section == "Build-Your-Own Playlist":
    st.title("Build Your Own Playlist")
    energy = st.slider("Energy Level", 0.0, 1.0, (0.4, 0.8))
    valence = st.slider("Mood (Valence)", 0.0, 1.0, (0.5, 0.9))
    tempo = st.slider("Tempo (BPM)", data_track["tempo"].min(), data_track["tempo"].max(), (90.0, 150.0),step= 1.0)
    playlist = data_track[
        (data_track["energy"] >= energy[0]) & (data_track["energy"] <= energy[1]) &
        (data_track["valence"] >= valence[0]) & (data_track["valence"] <= valence[1]) &
        (data_track["tempo"] >= tempo[0]) & (data_track["tempo"] <= tempo[1])
    ]
    st.subheader("Your Custom Playlist")
    st.write(playlist[[ "energy", "valence", "tempo"]])

# Section 6: Nostalgia Mode
elif section == "Nostalgia Mode: Hits from the Past":
    st.title("Nostalgia Mode: Hits from the Past")
    year = st.slider("Choose a Year", int(data["release_year"].min()), int(data["release_year"].max()), 2000)
    nostalgic_tracks = data[data["release_year"] == year].sort_values("popularity", ascending=False)
    fig = px.bar(
        nostalgic_tracks.head(10),
        x="track_title",
        y="popularity",
        color="artist",
        title=f"Top Tracks from {year}"
    )
    st.plotly_chart(fig)
    st.write(nostalgic_tracks[["track_title", "artist", "popularity", "release_date"]])

# Section 7: Audience Participation Predictor
elif section == "Audience Participation Predictor":
    st.title("Audience Participation Predictor")
    danceability = st.slider("Danceability", 0.0, 1.0, 0.5)
    energy = st.slider("Energy", 0.0, 1.0, 0.7)
    valence = st.slider("Valence (Mood)", 0.0, 1.0, 0.6)
    participation_score = (danceability * 0.4 + energy * 0.4 + valence * 0.2) * 100
    st.metric(label="Crowd Engagement", value=f"{int(participation_score)}%")
    if participation_score > 80:
        st.success("This track will get everyone dancing!")
    elif participation_score > 50:
        st.info("This track will have decent engagement.")
    else:
        st.warning("This track might not energize the crowd.")

# Section 8: Artist Duel
elif section == "Artist Duel: Who’s the Star?":
    st.title("Artist Duel: Who’s the Star?")
    artist_1 = st.selectbox("Choose Artist 1", data["artist"].unique())
    artist_2 = st.selectbox("Choose Artist 2", data["artist"].unique())
    artist_1_data = data[data["artist"] == artist_1]
    artist_2_data = data[data["artist"] == artist_2]
    duel_data = pd.DataFrame({
        "Metric": ["Popularity", "Followers", "Average Danceability", "Average Energy"],
        artist_1: [
            artist_1_data["popularity"].mean(),
            artist_1_data["followers"].mean(),
            artist_1_data["danceability"].mean(),
            artist_1_data["energy"].mean(),
        ],
        artist_2: [
            artist_2_data["popularity"].mean(),
            artist_2_data["followers"].mean(),
            artist_2_data["danceability"].mean(),
            artist_2_data["energy"].mean(),
        ],
    })
    fig = px.bar(
        duel_data.melt(id_vars="Metric", var_name="Artist", value_name="Score"),
        x="Metric",
        y="Score",
        color="Artist",
        barmode="group",
        title=f"Who’s the Star? {artist_1} vs {artist_2}"
    )
    st.plotly_chart(fig)
    st.write(duel_data)

# Section 9: Audio Feature Mashup
elif section == "Audio Feature Mashup":
    st.title("Audio Feature Mashup")
    feature_1 = st.selectbox("Feature 1", ["danceability", "energy", "valence", "acousticness"])
    feature_2 = st.selectbox("Feature 2", ["tempo", "loudness", "speechiness", "instrumentalness"])
    fig = px.scatter(
        data,
        x=feature_1,
        y=feature_2,
        size="popularity",
        hover_data=["track_title", "artist"],
        title=f"Audio Feature Mashup: {feature_1.capitalize()} vs {feature_2.capitalize()}",
        color="popularity",
        color_continuous_scale="Turbo"
    )
    st.plotly_chart(fig)
    standout = data[
        (data[feature_1] == data[feature_1].max()) | (data[feature_2] == data[feature_2].max())
    ]
    st.write(standout[["track_title", "artist", feature_1, feature_2, "popularity"]])
