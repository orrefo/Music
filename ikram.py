import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    # Page configuration
    st.set_page_config(
        page_title="Millennial Music Festival planning dashboard",
        page_icon="🎸",
        layout="wide"
    )



    # Header with custom styling
    st.markdown("""
        <style>
        .centered-image{
                display:block;
                margin-lef: auto;
                margin-right: auto;
        }        
        .big-title {
            font-size: 48px;
            font-weight: bold;
            color: #8839A1;
            text-align: center;
            margin-bottom: 20px;
        }
        .subtitle {
            font-size: 24px;
            color: #8839A1;
            text-align: center;
            margin-bottom: 40px;
        } 
        .quick-stats-title {
            font-size: 30px;
            color: #7e7e7e;
            margin-bottom: 10px;
            margin-left: 30px;
        }
        .quick-stats-subtext {
            font-size: 16px;
            color: #7e7e7e;
            margin-bottom: 5px;
            margin-left: 30px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    
    # Display an image from local file
    st.image("thumbnail.png", width=1200)

    st.markdown('<p class="big-title">Welcome to the 2026 Festival Lineup Planner</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Data-Driven Festival Planning Dashboard (2000-2024)</p>', unsafe_allow_html=True)
    st.markdown("---")

    # Main content columns
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### This dashboard is to help our client 'Live Nation Entertainment' organize their 2026 festival.
        
        - **Discover Top Artists from the last 25 years based on Billboard performance**
        - **Analyze Music Trends across different eras (2000-2024)**
        """)

        st.markdown("### Key Features")
        
        # Create three columns for features
        feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)
        
        with feat_col1:
            st.markdown("""
            🎵 **TrueReach**
            - TrueReach : Popularity score
            - Track Timeline
            """)
            
        with feat_col2:
            st.markdown("""
            🎯 **Artist Analysis**
            - Artist Insights
            - Top Artist Now
            """)

            
        with feat_col3:
            st.markdown("""
            📊 **Audio Feature**
            - Audio Trends by general statistics
            - Audio Trends by Artist specific statistics
            """)

        with feat_col4:
            st.markdown("""
            ⚔️ **Artist Duel**
            - Artist Duel : Who's the star?
            """)
    
    with col2:
        # Section 2: Quick Stats with styled text
        st.markdown('<p class="quick-stats-title">Quick Stats</p>', unsafe_allow_html=True)
        st.markdown('<p class="quick-stats-subtext">Data Timespan</p>', unsafe_allow_html=True)
        st.markdown('<p class="quick-stats-title">2000-2024</p>', unsafe_allow_html=True)
        st.markdown('<p class="quick-stats-subtext">Artists Database</p>', unsafe_allow_html=True)
        st.markdown('<p class="quick-stats-title">1000+ Artists</p>', unsafe_allow_html=True)
    # Bottom section
    st.markdown("---")
    st.markdown("### How to Use This Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        1️⃣ **TrueReach**
        - Choose the number of artists/ tracks to display
        - Select year range by artists/ tracks
        """)
        
    with col2:
        st.markdown("""
        2️⃣ **Artist Analysis**
        - Select an artist and discover their growth over time
        - See the artists most succesful tracks
        """)
        
    with col3:
        st.markdown("""
        3️⃣ **Audio Feature Trends**
        - Viewing general audio trends over time
        - Search artist's track to monitor audio trends
        """)

    with col4:
        st.markdown("""
        4️⃣ **Artist Duel**
        - Additional feature to compare two artists head-to-head
        - Compare various metrics between two artists
        """)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
    Developed using Billboard Charts (2000-2024) and Spotify Audio Features Data
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()