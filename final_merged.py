import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Load the dataset
@st.cache_data
def load_data():
    data = pd.read_csv("all.csv")
    return data
def merge_track(table_1,table_2):
    data=pd.merge(table_1,table_2,left_on='track_id',right_on='track_id',how='left')
    return data

def merge_artist(table_1,table_2):
    data=pd.merge(table_1,table_2,left_on='artist_id',right_on='artist_id',how='left')
    return data

data = load_data()

# Preprocess data: Group by artist to calculate the total points with the TrueReach system 
artist_scores = data.groupby("artist", as_index=False)["score"].sum()

# Sidebar Navigation
st.sidebar.title("🎵 Dashboard Navigation")
section = st.sidebar.radio(
    "Select a Section",
    [
        "🛬Landing Page",
        "👩‍🎤TrueReach®",
        "🎤 Artist Insights",
        "🔬Audio Features",
        "⚔️ Artist Duel: Who’s the Star?"
    ]
)
data["chart_week"] = pd.to_datetime(data["chart_week"], errors="coerce")

# Section 2: TrueReach
if section == "👩‍🎤TrueReach®":
    st.title("👩‍🎤TrueReach®")
    st.write(
        "See the songs and artists that we have loved through the years"
    )
    chart=pd.read_csv('chart.csv')
    mapping=pd.read_csv('mapping.csv',index_col=0)
    artist=pd.read_csv('artist.csv',index_col=0)
    tracks=pd.read_csv('tracks.csv',index_col=0)
    tracks=tracks.drop_duplicates()
    chart['score']=round((-15.79*np.log(chart['list_position']+1)+88.06)*1.3,0).astype('int')
    chart['chart_year']=pd.to_datetime(chart['chart_week']).dt.year
    map_artist=pd.merge(mapping,artist,left_on='artist_id',right_on='artist_id',how='left')
    artist_track=merge_track(map_artist,tracks)
    track_info=merge_track(tracks,artist_track.groupby(['track_id'])['name_x'].unique())
    track_info=merge_track(track_info,chart.groupby('track_id')['chart_week'].count())
    track_info=merge_track(track_info,chart.groupby('track_id')['chart_year'].min())
    track_info=merge_track(track_info,chart[chart['list_position']==1][['track_id','score']].groupby('track_id').count())
    data["chart_year"]=data['chart_week'].dt.year

    
    tab_1, tab_2=st.tabs(['Tracks','Artists'])
    with tab_1: 

        year_filter_yes = st.checkbox(
            "Single Year",
            value=False,
            help="Toggle to switch between single years or a range.")
        num=st.number_input('Number of songs to display',min_value=1,max_value=150,value=10)

        if year_filter_yes==False:
            min_year, max_year = chart["chart_year"].min(), chart["chart_year"].max()
            selected_years = st.slider(
                "Select Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                step=1,
                help="Drag the slider to filter tracks by year range.")
            
            filtered_data_2 = chart[
                (chart["chart_year"] >= selected_years[0]) &
                (chart["chart_year"] <= selected_years[1])]
            data_year=merge_track(filtered_data_2.groupby('track_id').sum().sort_values(by='score',ascending=False).head(num),track_info)
            data_year=data_year.rename(columns={
                'name':'track_title',
                'chart_week_y':'num_chart_appearence',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'name_x':'artist',
                'chart_year_y':'first_year_on_leaderboard' })
            
            fig= px.bar(data_year,x='track_title',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['track_title','TrueReach®','artist','first_year_on_leaderboard','num_chart_appearence','weeks_on_1st_place']])

        else:
            min_year, max_year = chart["chart_year"].min(), chart["chart_year"].max()
            selected_years = st.slider(
                "Select Year ",
                min_value=min_year,
                max_value=max_year,
                step=1,
                help="Drag the slider to filter tracks by year."
            )
            filtered_data_2 = chart[chart["chart_year"] == selected_years]
            data_year=merge_track(filtered_data_2.groupby('track_id').sum().sort_values(by='score',ascending=False).head(num),track_info)
            data_year=data_year.rename(columns={
                'name':'track_title',
                'chart_week_y':'num_chart_appearence',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'name_x':'artist',
                'chart_year_y':'first_year_on_leaderboard' })
            
            fig= px.bar(data_year,x='track_title',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['track_title','TrueReach®','artist','first_year_on_leaderboard','num_chart_appearence','weeks_on_1st_place']])
    with tab_2:

        year_filter_yes_art = st.checkbox(
        "Single Year",
        value=False,
        help="Toggle to switch between single years or a range for artists.")
        num_art=st.number_input('Amount of artists to display',min_value=1,max_value=150,value=10)

        if year_filter_yes_art==False:
            min_year, max_year = chart["chart_year"].min(), chart["chart_year"].max()
            selected_years_art = st.slider(
                "Select Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                step=1,
                help="Drag the slider to filter artists by year range.")
            
            filtered_data_3 = data[
                (data["chart_year"] >= selected_years_art[0]) &
                (data["chart_year"] <= selected_years_art[1])]
            data_year=merge_artist(filtered_data_3.groupby('artist_id')['score'].sum(),artist)
            data_year=merge_artist(data_year,filtered_data_3.groupby('artist_id')['track_title'].nunique())
            data_year=merge_artist(data_year,filtered_data_3.groupby('artist_id')['chart_week'].count())
            data_year=merge_artist(data_year,filtered_data_3.groupby('artist_id')['chart_year'].min())
            data_year=merge_artist(data_year,filtered_data_3[filtered_data_3['list_position']==1][['artist_id','score']].groupby('artist_id').count())
            data_year=data_year.sort_values(by='score_x',ascending=False).head(num_art).reset_index()        
            data_year=data_year.rename(columns={
                'name':'artist',
                'track_title':'songs_on_leaderboard',
                'chart_week':'num_chart_appearence',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'chart_year':'first_year_on_leaderboard',
                'popularity':'current_popularity' })
            
            fig= px.bar(data_year,x='artist',y='TrueReach®')
            st.plotly_chart(fig)
            st.write(data_year[['artist','TrueReach®','songs_on_leaderboard','num_chart_appearence','weeks_on_1st_place','first_year_on_leaderboard','current_popularity']])
            
        else:
            min_year, max_year = chart["chart_year"].min(), chart["chart_year"].max()
            selected_years_art = st.slider(
                "Select Year ",
                min_value=min_year,
                max_value=max_year,
                step=1,
                help="Drag the slider to filter artists by year.")
            
            filtered_data_4 = data[data["chart_year"] == selected_years_art]
            data_year=merge_artist(filtered_data_4.groupby('artist_id')['score'].sum(),artist)
            data_year=merge_artist(data_year,filtered_data_4.groupby('artist_id')['track_title'].nunique())
            data_year=merge_artist(data_year,filtered_data_4.groupby('artist_id')['chart_week'].count())
            data_year=merge_artist(data_year,filtered_data_4.groupby('artist_id')['chart_year'].min())
            data_year=merge_artist(data_year,filtered_data_4[filtered_data_4['list_position']==1][['artist_id','score']].groupby('artist_id').count())
            data_year=data_year.sort_values(by='score_x',ascending=False).head(num_art).reset_index()
            data_year=data_year.rename(columns={
                'name':'artist',
                'track_title':'songs_on_leaderboard',
                'chart_week':'num_chart_appearence',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'chart_year':'first_year_on_leaderboard',
                'popularity':'current_popularity' })
            
            fig= px.bar(data_year,x='artist',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['artist','TrueReach®','songs_on_leaderboard','num_chart_appearence','weeks_on_1st_place','current_popularity']])
            
            # Section 1: Artist Insights


elif section == "🎤 Artist Insights":
    st.title("🎤 Artist Insights")
    tab_1, tab_2=st.tabs(['Artist Insight','Top Artists Now'])
    with tab_1: 
        # Artist Filter
        st.subheader("Filter by Artist")
        artist_choice = st.selectbox("Select an Artist", data["artist"].unique())
        artist_data = data[data["artist"] == artist_choice]

        # Ensure data exists for the selected artist
        if artist_data.empty:
            st.write("No data available for the selected artist.")
        else:
            # 1. Artist Score Growth Over Time
            st.subheader("📈 Artist TrueReach® Growth Over Time")

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
            # Check if the artist has only one year of activity or no activity
        if min_year == max_year:
            st.write(f"The artist {artist_choice} has not been active across multiple years or has insufficient data for a range of years.")
        else:
            # Range slider for year selection
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
                title=f"TrueReach® Growth for {artist_choice} ({selected_years[0]} - {selected_years[1]})",
                labels={"Year": "Year", "score": "Score"},
                template="plotly_white"
            )
            fig.update_layout(title_x=0.5, xaxis=dict( type="category")) # Treat years as discrete categories to avoid decimals
        
            st.plotly_chart(fig, use_container_width=True)

            # 2. Most Successful Tracks by Chart Appearances
            st.subheader("Most Successful Tracks by Chart Appearances")
            track_success_count = (
                artist_data.groupby(["track_title", "artist"], as_index=False)
                .agg({"list_position": "count", "release_date": "min"})  # Count chart appearances and get release date
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

            # 3. Release Distribution
            st.subheader(f"Release Distribution for {artist_choice}")
            unique_tracks = artist_data.groupby("track_id", as_index=False).first()  # Ensure unique tracks by grouping on track_id
            track_types = unique_tracks["album_type"].value_counts().reset_index()
            track_types.columns = ["album_type", "count"]

            fig = px.pie(
                track_types,
                values="count",
                names="album_type",
                title=f"Release Distribution for {artist_choice}",
                labels={"album_type": "Album Type", "count": "Count"},
                template="plotly_white"
            )
            st.plotly_chart(fig)
    with tab_2: 
        # Discover Top Artists
            
        st.subheader("Discover the Top Artists Now")
        st.write("Explore the top artists based on current popularity and customize filters to refine the view.")

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
                "score": "sum"         # Total score for the artist (TrueReach)
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
    st.subheader("🌟 TrueReach® Comparison")
    overall_score_data = pd.DataFrame({
        "Artist": [artist_1, artist_2],
        "Score": [artist_1_score, artist_2_score]
    })
    fig = px.bar(
        overall_score_data,
        x="Artist",
        y="Score",
        title="🌟 TrueReach® Comparison",
        labels={"Artist": "Artist", "Score": "TrueReach®"},
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

        # Transform values for specific metrics
        if metric_column in ["danceability", "energy", "valence"]:
            artist_1_score = artist_1_data[metric_column].mean() * 100
            artist_2_score = artist_2_data[metric_column].mean() * 100
        else:
            artist_1_score = artist_1_data[metric_column].mean()
            artist_2_score = artist_2_data[metric_column].mean()

        # Create a DataFrame for the metric comparison
        duel_data = pd.DataFrame({
            "Artist": [artist_1, artist_2],
            "Score": [artist_1_score, artist_2_score]
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


    # Prepare summary table
    st.subheader("📊 Summary of Comparison Metrics")
    summary_data = pd.DataFrame({
        "Metric": ["🌟 TrueReach®"] + list(metrics.keys()),
        artist_1: [artist_1_score] + [
            round(artist_1_data[metrics[key]].mean() * 100, 1) if metrics[key] in ["danceability", "energy", "valence"] else round(artist_1_data[metrics[key]].mean(), 1)
            for key in metrics
        ],
        artist_2: [artist_2_score] + [
            round(artist_2_data[metrics[key]].mean() * 100, 1) if metrics[key] in ["danceability", "energy", "valence"] else round(artist_2_data[metrics[key]].mean(), 1)
            for key in metrics
        ]
    })

    # Display summary table
    st.dataframe(summary_data, use_container_width=True)


