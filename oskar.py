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
        "Track Insights",
        "Festival Lineup Optimizer"
    ]    
)


# Section 2: Track Insights
if section == "Track Insights":
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
        filtered_lineup = data[data["energy"] <= 0.4]
    elif time_of_day == "Afternoon":
        filtered_lineup = data[(data["energy"] > 0.4) & (data["energy"] <= 0.6)]
    elif time_of_day == "Evening":
        filtered_lineup = data[(data["energy"] > 0.6) & (data["energy"] <= 0.8)]
    else:
        filtered_lineup = data[data["energy"] > 0.8]

    st.write(f"Recommended Artists and Tracks for {time_of_day}")
    st.write(filtered_lineup[["artist", "track_title", "energy", "valence"]])


