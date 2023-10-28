import os
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Fetch API key from environment variable
API_KEY = 'AIzaSyCn2UfhhnTJbBRcACQ0g6bh1hpZfmRgqhM'


def get_playlist_details(playlist_id, youtube):
    try:
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()

        if 'items' in playlist_response and len(playlist_response['items']) > 0:
            playlist_info = playlist_response['items'][0]['snippet']
            playlist_title = playlist_info['title']
            playlist_description = playlist_info['description']
            return playlist_title, playlist_description

        else:
            print("Playlist not found.")
            return None, None

    except HttpError as e:
        print(f"An error occurred while fetching playlist details: {str(e)}")
        return None, None

def get_playlist_items(playlist_id, youtube):
    playlist_items = []
    next_page_token = None

    try:
        while True:
            playlist_response = youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()

            for item in playlist_response['items']:
                video_id = item['snippet']['resourceId']['videoId']
                video_details = get_video_details(video_id, youtube)
                if video_details:
                    playlist_items.append(video_details)

            next_page_token = playlist_response.get('nextPageToken')

            if not next_page_token:
                break

    except HttpError as e:
        print(f"An error occurred while fetching playlist items: {str(e)}")

    return playlist_items

def get_video_details(video_id, youtube):
    try:
        video_response = youtube.videos().list(
            part='snippet,contentDetails',
            id=video_id
        ).execute()

        video_info = video_response['items'][0]

        video_details = {
            'title': video_info['snippet']['title'],
            'description': video_info['snippet']['description'],
            'embed_link': f"https://www.youtube.com/watch?v={video_id}",
            'duration': video_info['contentDetails']['duration']
        }

        return video_details

    except HttpError as e:
        print(f"An error occurred while fetching video details: {str(e)}")
        return None

def format_full_data(playlist_id, playlist_title, playlist_items):
    full_data = {
        '_id': playlist_id,
        'title': playlist_title,
        'Playlist_link': f"https://www.youtube.com/playlist?list={playlist_id}",
        'Playlist_img': '',  # You can fill this field as needed
        'data': [
            {
                'tittle' : '',
                'content': playlist_items
            }
        ]
    }


    return full_data


def format_partial_data(playlist_id, playlist_title, playlist_description, playlist_items):
    partial_data = {
        '_id': playlist_id,
        'PlaylistLink': f"https://www.youtube.com/playlist?list={playlist_id}",
        'title': playlist_title,
        'tags': [],
        'review': None,
        'review_numer': None,
        'language': '',
        'author': '',
        'duration': '',  # You can calculate the total duration of videos later
        'description': playlist_description  # Use the fetched description here
    }

    return partial_data

def format_third_data(playlist_items):
    third_data = []

    for video_details in playlist_items:
        third_data.append({
            'title': video_details['title']
        })

    return third_data

def main():
    playlist_id = input("Enter the YouTube playlist ID: ")
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    
    # Fetch playlist details
    playlist_title, playlist_description = get_playlist_details(playlist_id, youtube)

    if not playlist_title:
        print("Playlist details not found.")
        return

    playlist_items = get_playlist_items(playlist_id, youtube)

    if not playlist_items:
        print("No videos found in the playlist.")
        return

    full_data = format_full_data(playlist_id, playlist_title, playlist_items)
    partial_data = format_partial_data(playlist_id, playlist_title, playlist_description, playlist_items)
    third_data = format_third_data(playlist_items)

    full_data_output_file = f"a.json"
    partial_data_output_file = f"b.json"
    third_data_output_file = f"c.json"

    with open(full_data_output_file, 'w', encoding='utf-8') as full_file:
        json.dump(full_data, full_file, ensure_ascii=False, indent=4)

    with open(partial_data_output_file, 'w', encoding='utf-8') as partial_file:
        json.dump(partial_data, partial_file, ensure_ascii=False, indent=4)

    with open(third_data_output_file, 'w', encoding='utf-8') as third_file:
        json.dump(third_data, third_file, ensure_ascii=False, indent=4)

    print(f"Full data has been saved to {full_data_output_file}.")
    print(f"Partial data has been saved to {partial_data_output_file}.")
    print(f"Third data has been saved to {third_data_output_file}.")

if __name__ == "__main__":
    main()
