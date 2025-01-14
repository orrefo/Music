import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

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

# Preprocess data: Group by artist to calculate the total points 
artist_scores = data.groupby("artist", as_index=False)["score"].sum()


# Sidebar Navigation
st.sidebar.title("🎵 Dashboard Navigation")
section = st.sidebar.radio(
    "Select a Section",
    [
        "🎤 Artist Insights",
        "👩‍🎤TrueReach®"
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
        fig.update_layout(title_x=0.5, template="plotly_white")
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

    grouped_artists = data.groupby("artist", as_index=False).agg({
        "popularity": "mean",  # Average popularity score
        "followers": "sum",    # Total followers for each artist
        "explicit": "any",     # Check if any track is explicit
        "score": "sum"         # Total score for the artist
    })

    # Apply filters
    filtered_artists = grouped_artists[grouped_artists['popularity'] >= popularity_threshold]
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




# Section 2: TrueReach
elif section == "👩‍🎤TrueReach®":
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
                'chart_week_y':'weeks_on_leaderboard',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'name_x':'artist',
                'chart_year_y':'first_year_on_leaderboard' })
            
            fig= px.bar(data_year,x='track_title',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['track_title','TrueReach®','artist','first_year_on_leaderboard','weeks_on_leaderboard','weeks_on_1st_place']])

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
                'chart_week_y':'weeks_on_leaderboard',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'name_x':'artist',
                'chart_year_y':'first_year_on_leaderboard' })
            
            fig= px.bar(data_year,x='track_title',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['track_title','TrueReach®','artist','first_year_on_leaderboard','weeks_on_leaderboard','weeks_on_1st_place']])
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
                'chart_week':'weeks_on_leaderboard',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'chart_year':'first_year_on_leaderboard',
                'popularity':'current_popularity' })
            
            fig= px.bar(data_year,x='artist',y='TrueReach®')
            st.plotly_chart(fig)
            st.write(data_year[['artist','TrueReach®','songs_on_leaderboard','weeks_on_leaderboard','weeks_on_1st_place','first_year_on_leaderboard','current_popularity']])
            
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
                'chart_week':'weeks_on_leaderboard',
                'score_y':'weeks_on_1st_place',
                'score_x':'TrueReach®',
                'chart_year':'first_year_on_leaderboard',
                'popularity':'current_popularity' })
            
            fig= px.bar(data_year,x='artist',y='TrueReach®',text_auto='.2s')
            st.plotly_chart(fig)
            st.write(data_year[['artist','TrueReach®','songs_on_leaderboard','weeks_on_leaderboard','weeks_on_1st_place','first_year_on_leaderboard','current_popularity']])
            