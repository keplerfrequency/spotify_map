import json

def display_playlists():
    with open('playlist.json') as f:
        data = json.load(f)

    country_playlist = {}
    for country in data['countries']:
        for playlist in country['playlists']:
            country_playlist[country['country']] = country_playlist.get(country['country'], [])
            country_playlist[country['country']].append(playlist)

    html = ''
    for country, playlists in country_playlist.items():
        html += f'<li id="{country}" class="country">\n'
        for playlist in playlists:
            html += '<div class="playlist_card" loading="lazy">\n'
            html += f'<a href="{playlist["link"]}" target="_blank" rel="noopener noreferrer">\n'
            html += f'<img class="playlist-img" loading="lazy" src="{playlist["img"]}" data-href="{playlist["link"]}">\n'
            html += '</a>'
            html += f'<p>{playlist["name"]}</p>\n'
            html += f'<p1>{playlist["playlist_by"]}</p1>\n'
            html += f'<div class="playlist_description">{playlist["description"]}</div>'
            html += '</div>'
        html += '</li>'
    html += '<div id="buffer_area"></div>'

    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
    index_html = index_html.replace('<ul id="playlists" class="playlists"></ul>', f'<ul id="playlists" class="playlists">\n{html}</ul>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

def main():

    display_playlists()


if __name__ == '__main__':
    main()