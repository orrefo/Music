import streamlit as st
import pandas as pd
from datetime import datetime

def main():
    # Page configuration
    st.set_page_config(
        page_title="Lollapalooza Nostalgia Planner",
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

if __name__ == "__main__":
    main()