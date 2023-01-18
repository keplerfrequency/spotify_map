import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pycountry
import json
import numpy as np

CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
CLIENT_SECRET = 'f1805609facd442197c8520f6152ae11'
OUTPUT_JSON = "test_output_playlists.json"

#Do a search of the playslists
def get_playlists(query, type, limit, market):

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, ))

    return spotify.search(query, limit, 0, type, market)

#Run through all countries and get 'limit' playlists for each one
def go_through_countries():
    
    #Search parameters
    europe_countries = ["albania","andorra","austria","belarus","belgium","bosnia","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","san marino","italy","kosovo","latvia","liechtenstein","lithuania","luxembourg","macedonia","malta", "moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","russia","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","united kingdom"]
    europe_countries = ["spain"]
    type = "playlist"
    limit = 5
    
    for country in europe_countries:
        
        #Get country code for coutnry. needed for market search 
        codes = pycountry.countries.search_fuzzy(country)
        market = str(codes)[18] + str(codes)[19]
        print("{} {}".format(market, country))
        playlists = get_playlists(country, type, limit, market)

        #dump response in json file with all platlists found
        with open(OUTPUT_JSON, "a") as outfile:
            json.dump(playlists, outfile)
    
    return

def main():

    go_through_countries()

    f = open('test_output_playlists.json')

    data = json.load(f)

    list_of_playlists=[None]*4


    for item in data['playlists']['items']:
        country = "a"
        urls = item["external_urls"]['spotify']
        display_name = item["owner"]["display_name"]
        name= item["name"]

        array = [country, urls, display_name, name]
        list_of_playlists = np.vstack((array, list_of_playlists))
        
    list_of_playlists=list_of_playlists[:-1, :] 
    list_of_playlists=list_of_playlists[np.argsort(list_of_playlists[:,2])]
    print(list_of_playlists)

    f.close()

    





    
    
   


if __name__ == '__main__':
    main()
    