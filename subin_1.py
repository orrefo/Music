import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime


# Spotify API Credentials
CLIENT_ID = '0d697f8623514a3497f61073c92b49f9'
CLIENT_SECRET = '802be2833fc942469293557fe6d253b8'
# Initialize Spotify API client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

# Function to fetch artist image
@st.cache_data
def get_artist_image(artist_name):
    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results.get('artists', {}).get('items', [])
    if items:
        return items[0].get('images', [])[0].get('url')
    return None

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("https://raw.githubusercontent.com/orrefo/Music/refs/heads/main/all.csv")
    return data

data = load_data()

# Ensure "chart_week" is in datetime format
data["chart_week"] = pd.to_datetime(data["chart_week"], errors="coerce")

# Sidebar Navigation
st.sidebar.title(":musical_note: Dashboard Navigation")
section = st.sidebar.radio(
    "Select a Section",
    ['Main', "True reach", ":musical_note: Audio Feature Trends", "Artist insight", "Artist Duel"]
)

# Landing page
def main():
    # Page configuration
    st.set_page_config(
        page_title="When We Were Young Festival",
        page_icon="🎸",
        layout="wide"
    )

    # Header with custom styling
    st.markdown("""
        <style>
        .big-title {
            font-size: 48px;
            font-weight: bold;
            color: #1DB954;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #666;
            text-align: center;
            margin-bottom: 40px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<p class="big-title">Lollapalooza Nostalgia Edition</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Data-Driven Festival Planning Dashboard (2000-2024)</p>', unsafe_allow_html=True)

    # Main content columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### About This Dashboard
        Welcome to the Lollapalooza Nostalgia Edition Planning Tool! This interactive dashboard helps festival organizers:
        
        - **Discover Top Artists** from the last 25 years based on Billboard performance
        - **Analyze Music Trends** across different eras (2000-2024)
        - **Optimize Stage Planning** using audio features and popularity metrics
        - **Create Balanced Lineups** across genres and time periods
        """)

        st.markdown("### Key Features")
        
        # Create three columns for features
        feat_col1, feat_col2, feat_col3 = st.columns(3)
        
        with feat_col1:
            st.markdown("""
            🎯 **Artist Analysis**
            - Historical performance
            - Current popularity
            - Fan following
            """)
            
        with feat_col2:
            st.markdown("""
            🎵 **Music Insights**
            - Genre distribution
            - Audio characteristics
            - Era popularity
            """)
            
        with feat_col3:
            st.markdown("""
            📊 **Planning Tools**
            - Stage allocation
            - Time slot optimizer
            - Audience flow prediction
            """)

    with col2:
        st.markdown("### Quick Stats")
        
        # Placeholder metrics (you'll replace these with actual data)
        st.metric("Data Timespan", "2000-2024")
        st.metric("Artists Database", "1000+ Artists")
        st.metric("Tracked Features", "15+ Metrics")
        
        # Add a simple form for quick artist search
        st.markdown("### Quick Artist Search")
        search_term = st.text_input("Enter artist name")
        if search_term:
            st.info("Navigate to the Artist Analysis page to see detailed information")

    # Bottom section
    st.markdown("---")
    st.markdown("### How to Use This Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        1️⃣ **Artist Selection**
        - Search for artists by era
        - Filter by popularity metrics
        - Analyze historical performance
        """)
        
    with col2:
        st.markdown("""
        2️⃣ **Stage Planning**
        - View compatibility scores
        - Check artist scheduling
        - Optimize crowd flow
        """)
        
    with col3:
        st.markdown("""
        3️⃣ **Analytics**
        - Track genre distribution
        - Monitor popularity trends
        - Generate reports
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    Developed using Billboard Charts (2000-2024) and Spotify Audio Features Data
    </div>
    """, unsafe_allow_html=True)

if section == "__main__":
    main()

# Section: True Reach
elif section == "True reach":
    st.title("True reach : Who is going to be our headliners?")
    st.write("Coming soon...")  # Placeholder content

# Section: Artist Insight
elif section == "Artist insight":
    st.title("Artist insight")
    st.write("Coming soon...")  # Placeholder content


# Section: Audio Feature Trends
elif section == ":musical_note: Audio Feature Trends":
    st.title(":musical_note: Audio Feature Trends Over Time")

    # List of audio features to plot
    audio_features = [
        "acousticness",
        "valence",
        "danceability",
        "energy",
        "speechiness",
        "instrumentalness",
        "liveness"
    ]

    # Dictionary of audio features and their corresponding emojis
    feature_emojis = {
        "acousticness": ":guitar:",  # Guitar
        "valence": ":smiley:",       # Smiley face
        "danceability": ":man_dancing:",  # Dancer
        "energy": ":zap:",             # Lightning bolt
        "speechiness": ":speaking_head_in_silhouette:",  # Speaking head
        "instrumentalness": ":musical_keyboard:",  # Keyboard
        "liveness": ":microphone:"        # Microphone
    }

    # Check if the dataset contains the necessary columns
    available_features = [feature for feature in audio_features if feature in data.columns]

    if not available_features:
        st.error("The dataset does not contain any of the specified audio features.")
    elif data["chart_week"].isna().all():
        st.error("The 'chart_week' column contains no valid dates.")
    else:
        # Filter data to ensure non-missing values for "chart_week"
        valid_data = data.dropna(subset=["chart_week"])

        # Iterate through each audio feature
        for feature in available_features:
            # Get the corresponding emoji for the feature
            emoji = feature_emojis.get(feature, "")

            # Filter data for the current feature
            feature_data = valid_data.dropna(subset=[feature])

            # Group by "track_title" to calculate maximum values
            grouped_tracks = feature_data.groupby("track_title").agg(
                {
                    feature: "max",  # Maximum value of the feature
                    "artist": "first",  # Keep the first occurrence of the artist
                    "score": "max"  # Maximum score
                }
            ).reset_index()

            # Sort by "score" and feature value in descending order
            top_tracks = grouped_tracks.sort_values(
                by=["score", feature], ascending=[False, False]
            ).head(10)

            # Create a trend graph for the audio feature
            feature_trend = (
                feature_data.groupby(feature_data["chart_week"].dt.year)
                .agg({feature: "mean"})
                .reset_index()
                .rename(columns={"chart_week": "Year", feature: f"Average {feature.capitalize()}"})
            )

            fig = px.line(
                feature_trend,
                x="Year",
                y=f"Average {feature.capitalize()}",
                title=f"Trend of {feature.capitalize()} Over Time {emoji} by TrueReach®",
                labels={"Year": "Year", f"Average {feature.capitalize()}": feature.capitalize()},
                template="plotly_white"
            )
            fig.update_layout(
                title_x=0.5,
                xaxis=dict(
                    title="Year",
                    tickfont=dict(size=20)
                ),
                yaxis=dict(
                    title=f"Average {feature.capitalize()}",
                    tickfont=dict(size=16)
                ),
                font=dict(size=14)
            )

            # Display the plot
            st.plotly_chart(fig, use_container_width=True)

            # Display the top 10 tracks table with artist images
            st.subheader(f"Top 10 Tracks by {feature.capitalize()} {emoji} by TrueReach®")
            top_tracks = top_tracks[["track_title", "artist", feature, "score"]]
            top_tracks = top_tracks.rename(columns={
                "track_title": "Track Title",
                "artist": "Artist",
                feature: f"{feature.capitalize()}",
                "score": "Score"
            }).reset_index(drop=True)

            for i in range(0, len(top_tracks), 5):
                cols = st.columns(5)
                for col, (idx, row) in zip(cols, top_tracks.iloc[i:i+5].iterrows()):
                    artist_image_url = get_artist_image(row["Artist"])
                    if artist_image_url:
                        col.image(artist_image_url, width=220)
                    col.write(f"**Track:** {row['Track Title']}")
                    col.write(f"**Artist:** {row['Artist']}")
                    col.write(f"**{feature.capitalize()}:** {row[feature.capitalize()]}")
                    col.write(f"**Score:** {row['Score']}")



# Section: Artist Duel
elif section == "Artist Duel":
    st.title("Artist Duel : Compare the artists")
    st.write("Coming soon...")  # Placeholder content
