import streamlit as st
import pandas as pd
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