import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pycountry
import json
import numpy as np
import os
import shutil

CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
CLIENT_SECRET = 'f1805609facd442197c8520f6152ae11'
OUTPUT_JSON = "test_output_playlists.json"
PLAYLIST_JSON = "playlist.json"
TEMP_PLAYLIST_JSON = "temp_playlist.json"
NUMBER_OF_PLAYLISTS = 15

#Do a search of the playslists
def get_playlists(query, type, limit, market):

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, ))

    valid_markets = ["AD","AE","AG","AL","AM","AO","AR","AT","AU","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BN","BO","BR","BS","BT","BW","BY","BZ","CA","CD","CG","CH","CI","CL","CM","CO","CR","CV","CW","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","ES","ET","FI","FJ","FM","FR","GA","GB","GD","GE","GH","GM","GN","GQ","GR","GT","GW","GY","HK","HN","HR","HT","HU","ID","IE","IL","IN","IQ","IS","IT","JM","JO","JP","KE","KG","KH","KI","KM","KN","KR","KW","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MG","MH","MK","ML","MN","MO","MR","MT","MU","MV","MW","MX","MY","MZ","NA","NE","NG","NI","NL","NO","NP","NR","NZ","OM","PA","PE","PG","PH","PK","PL","PS","PT","PW","PY","QA","RO","RS","RW","SA","SB","SC","SE","SG","SI","SK","SL","SM","SN","SR","ST","SV","SZ","TD","TG","TH","TJ","TL","TN","TO","TR","TT","TV","TW","TZ","UA","UG","US","UY","UZ","VC","VE","VN","VU","WS","XK","ZA","ZM","ZW"]

    if market in valid_markets:
        try:
            response = spotify.search(query, limit, 0, type, market)
        except:
            pass
        return response
    else:
        print("{} failed. Check support for market".format(query))
        return

#Get the playlists from a country
def request_playlist(country):
    
    type = "playlist"
    limit = NUMBER_OF_PLAYLISTS
        
    #Get country code for coutnry. needed for market search 
    codes = pycountry.countries.search_fuzzy(country)
    market = str(codes)[18] + str(codes)[19]
    
    print("{} {}".format(market, country))
    
    #Actually perform search
    playlists = get_playlists(country, type, limit, market)

    #Dump response in json file with all playlists found for country
    with open(OUTPUT_JSON, "w") as outfile:
        json.dump(playlists, outfile)

    return


def go_through_response(country):
    
    #open file where the playlist is for country X and load in JSON
    f = open(OUTPUT_JSON)
    data = json.load(f)

    #Initialize list of playlists for country X
    list_of_playlists=[None]*4

    for item in data['playlists']['items']:
        urls = item["external_urls"]['spotify']
        display_name = item["owner"]["display_name"]
        name= item["name"]

        array = [country, urls, display_name, name]
        list_of_playlists = np.vstack((array, list_of_playlists))
        
    #List by name so that similalry named lists appear together (BROKEN)
    #list_of_playlists=np.sort(list_of_playlists, axis=1)
    
    f.close()

    return list_of_playlists


def fill_playlist_json(list_of_all_playlists):

    json_schema = {
        "countries": []
        }

    with open(TEMP_PLAYLIST_JSON, 'a') as json_file:
        for row in range(np.shape(list_of_all_playlists)[0]):
            country = {
                "country": list_of_all_playlists[row, 0],
                "playlists": [{
                    "link": list_of_all_playlists[row, 1],
                    "playlist_by": list_of_all_playlists[row, 2],
                    "name": list_of_all_playlists[row, 3]
                }]
            }
            json_schema['countries'].append(country)
        json.dump(json_schema, json_file, indent=4, separators=(',', ': '))
    
    return

def main():

    #Countries
    europe_countries = ["albania","andorra","austria","belarus","belgium","bosnia","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","san marino","italy","kosovo","latvia","liechtenstein","lithuania","luxembourg","macedonia","malta", "moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","russia","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","united kingdom"]
    #no russia
    europe_countries = ["albania","andorra","austria","belarus","belgium","bosnia","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","san marino","italy","kosovo","latvia","liechtenstein","lithuania","luxembourg","macedonia","malta", "moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","united kingdom"]
    
    list_of_all_playlists=[None]*4

    for country in europe_countries:
        
        #Get the playlists from country X
        request_playlist(country)

        playlists = go_through_response(country)
        
        #print(playlists)
        list_of_all_playlists = np.vstack((list_of_all_playlists, playlists))

        #Remove line of nones
        list_of_all_playlists = np.delete(list_of_all_playlists, (-1), axis=0)


    list_of_all_playlists = np.delete(list_of_all_playlists, (0), axis=0)
    print(list_of_all_playlists)

    #fill the list with all the players
    fill_playlist_json(list_of_all_playlists)

    if os.path.exists(PLAYLIST_JSON):
        os.remove(PLAYLIST_JSON)

    if os.path.exists(TEMP_PLAYLIST_JSON):
        shutil.copyfile(TEMP_PLAYLIST_JSON, PLAYLIST_JSON)    
        os.remove(TEMP_PLAYLIST_JSON)
    





    
    
   


if __name__ == '__main__':
    main()
    