import streamlit as st
import requests
from datetime import datetime, timedelta
import os

# YouTube API Key (use environment variable or Streamlit secrets)
API_KEY = os.getenv("AIzaSyDp5L0O_tdYbfV4iX_iH5JcNa37cvxxUsc")  # or use st.secrets["AIzaSyDp5L0O_tdYbfV4iX_iH5JcNa37cvxxUsc"]
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
                "maxResults": 5,
                "key": API_KEY,
            }  # Closing brace for search_params dictionary

            # Fetch video data
            response = requests.get(YOUTUBE_SEARCH_URL, params=search_params)
            if response.status_code != 200:
                st.error(f"Failed to fetch data for keyword: {keyword}. Status code: {response.status_code}")
                continue

            data = response.json()
            if "items" not in data or not data["items"]:
                st.warning(f"No videos found for keyword: {keyword}")
                continue

            videos = data["items"]
            video_ids = [video["id"].get("videoId") for video in videos if "id" in video]
            channel_ids = [video["snippet"].get("channelId") for video in videos if "snippet" in video]

            if not video_ids or not channel_ids:
                st.warning(f"No valid video or channel data found for keyword: {keyword}")
                continue

            # Fetch video statistics
            stats_params = {"part": "statistics", "id": ",".join(video_ids), "key": API_KEY}
            stats_response = requests.get(YOUTUBE_VIDEO_URL, params=stats_params)
            if stats_response.status_code != 200:
                st.error(f"Failed to fetch video statistics for keyword: {keyword}")
                continue

            stats_data = stats_response.json()
            if "items" not in stats_data or not stats_data["items"]:
                st.warning(f"No video statistics found for keyword: {keyword}")
                continue

            # Fetch channel statistics
            channel_params = {"part": "statistics", "id": ",".join(channel_ids), "key": API_KEY}
            channel_response = requests.get(YOUTUBE_CHANNEL_URL, params=channel_params)
            if channel_response.status_code != 200:
                st.error(f"Failed to fetch channel statistics for keyword: {keyword}")
                continue

            channel_data = channel_response.json()
            if "items" not in channel_data or not channel_data["items"]:
                st.warning(f"No channel statistics found for keyword: {keyword}")
                continue

            stats = stats_data["items"]
            channels = channel_data["items"]

            # Collect results
            for video, stat, channel in zip(videos, stats, channels):
                title = video["snippet"].get("title", "N/A")
                description = video["snippet"].get("description", "")[:200]
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                views = int(stat["statistics"].get("viewCount", 0))
                subs = int(channel["statistics"].get("subscriberCount", 0))

                if subs < 3000:  # Only include channels with fewer than 3,000 subscribers
                    all_results.append({
                        "Title": title,
                        "Description": description,
                        "URL": video_url,
                        "Views": views,
                        "Subscribers": subs
                    })  # Closing brace for all_results.append dictionary

        # Display results
        if all_results:
            st.success(f"Found {len(all_results)} results across all keywords!")
            st.dataframe(all_results)
        else:
            st.warning("No results found for channels with fewer than 3,000 subscribers.")

    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
    except KeyError as e:
        st.error(f"Missing expected data in API response: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
