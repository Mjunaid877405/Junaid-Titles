import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# Securely fetching the API key from environment variables
API_KEY = os.getenv("AIzaSyD1yebvf2bpu0A9E6v4w5MhRzGGmaSG7Io")

# URLs for YouTube Data API v3
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_VIDEO_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_CHANNEL_URL = "https://www.googleapis.com/youtube/v3/channels"

# Streamlit app title
st.title("Junaid's Titles")

# User input for days
days = st.number_input("Enter Days to Search (1-30):", min_value=1, max_value=30, value=5)

# List of cat-related keywords
keywords = [
    "Cat Behavior", "Cat Health", "Feline Psychology", "cat tips", 
    "Cat facts", "Cat Owners", "cat parents", "Cat Love Signs", "Cat Bonding", 
    "Male cats", "Indoor Cat Care", "Cat Body Language", "Cat Emotional Health", 
    "Cat Personality", "Cat Happiness", "Cat Cuddles", 
    "Cat Personal Space", "Cat Protection", "cat love", 
    "indoor cat", "Cats Trust", "happy cat", 
    "Unlove signs"
]

# Button to fetch data from YouTube
if st.button("Fetch Data"):
    try:
        # Calculate the start date based on user input
        start_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")
        all_results = []

        # Loop over each keyword and make API calls
        for keyword in keywords:
            search_params = {
                "part": "snippet",
                "q": keyword,
                "type": "video",
                "order": "viewCount",
                "publishedAfter": start_date,
                "maxResults": 5,
                "key": API_KEY,
            }

            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            if response.status_code == 200:
                videos = response.json().get("items", [])
                for video in videos:
                    video_id = video["id"]["videoId"]
                    channel_id = video["snippet"]["channelId"]

                    stats_response = requests.get(YOUTUBE_VIDEO_URL, params={"part": "statistics", "id": video_id, "key": API_KEY})
                    channel_response = requests.get(YOUTUBE_CHANNEL_URL, params={"part": "statistics", "id": channel_id, "key": API_KEY})

                    if stats_response.status_code == 200 and channel_response.status_code == 200:
                        video_stats = stats_response.json().get("items", [{}])[0]
                        channel_stats = channel_response.json().get("items", [{}])[0]
                        title = video["snippet"].get("title", "N/A")
                        description = video["snippet"].get("description", "")[:200]
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        views = int(video_stats["statistics"].get("viewCount", 0))
                        subs = int(channel_stats["statistics"].get("subscriberCount", 0))

                        if subs < 3000:
                            all_results.append({
                                "Title": title,
                                "Description": description,
                                "URL": video_url,
                                "Views": views,
                                "Subscribers": subs
                            })
            else:
                st.error(f"Failed to fetch data for keyword: {keyword}. Status code: {response.status_code}")

        # Display results if any
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            st.dataframe(all_results)
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
