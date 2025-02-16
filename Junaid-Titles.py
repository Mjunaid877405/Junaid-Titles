import requests

API_KEY = 'AIzaSyD1yebvf2bpu0A9E6v4w5MhRzGGmaSG7Io'
CHANNEL_ID = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'  # This is a public YouTube channel ID for testing

def test_youtube_api(api_key):
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        'part': 'snippet,contentDetails,statistics',
        'id': CHANNEL_ID,
        'key': api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("API Key is working, response data:", response.json())
    else:
        print("Failed to fetch data, status code:", response.status_code)

test_youtube_api(API_KEY)
