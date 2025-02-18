# Script made to extract original Spotify playlists

import json

PLAYLIST = "spotify_playlists.json"
PLAYLIST_FILTERED = "spotify_filtered_playlists.json"

# Function to filter playlists
def filter_playlists(data):
    for country in data['countries']:
        country['playlists'] = [playlist for playlist in country['playlists'] if playlist['playlist_by'] == "Spotify"]
    
    # Filter empty parts
    data['countries'] = [country for country in data['countries'] if country['playlists']]
    
    return data

# Read the file
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def main():
    
    data = read_json_file(PLAYLIST)

    filtered_data = filter_playlists(data)

    # Write the filtered data to a new JSON file
    with open(PLAYLIST_FILTERED, 'w') as json_file:
        json.dump(filtered_data, json_file, indent=4)

if __name__ == '__main__':
    main()