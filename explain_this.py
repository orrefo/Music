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
            