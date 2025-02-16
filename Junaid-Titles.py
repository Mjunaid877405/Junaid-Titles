import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# YouTube API Key (use environment variable or Streamlit secrets)
API_KEY = os.getenv("AIzaSyDp5L0O_tdYbfV4iX_iH5JcNa37cvxxUsc")  # or use st.secrets["YAIzaSyDp5L0O_tdYbfV4iX_iH5JcNa37cvxxUsc"]
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit App Title
st.title("YouTube Viral Topics Tool")

# Input Fields
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of broader keywords
keywords = [
    "Affair Relationship Stories", "Reddit Update", "Reddit Relationship Advice", 
    "Reddit Relationship", "Reddit Cheating", "AITA Update", "Open Marriage", 
    "Open Relationship", "X BF Caught", "Stories Cheat", "X GF Reddit", 
    "AskReddit Surviving Infidelity", "GurlCan Reddit", "Cheating Story Actually Happened", 
    "Cheating Story Real", "True Cheating Story", "Reddit Cheating Story", 
    "R/Surviving Infidelity", "Surviving Infidelity", "Reddit Marriage", 
    "Wife Cheated I Can't Forgive", "Reddit AP", "Exposed Wife", "Cheat Exposed"
]

# Fetch Data Button
if st.button("Fetch Data"):
    try:
        # Calculate date range
        start_date = (datetime.utcnow() - timedelta(days=int(days))).strftime("%Y-%m-%dT%H:%M:%SZ")
        all_results = []

        # Iterate over the list of keywords
        for keyword in keywords:
            st.write(f"Searching for keyword: {keyword}")

            # Define search parameters
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5
