import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pycountry
import json
import numpy as np
import os
import shutil

#Get this here: https://developer.spotify.com/dashboard/applications
CLIENT_ID = '948c4e2f99254fcdbf7e8f9779da03b6'
CLIENT_SECRET = '31711ce22be54da09b8aabe950c42b09'
#Output JSON is where the response from spotify is temporarily stored and then removed 
OUTPUT_JSON = "test_output_playlists.json"
#Playlist.json file is where all the playlists are stored. the temp is a temp file that then overwrites the other one
PLAYLIST_JSON = "playlist.json"
TEMP_PLAYLIST_JSON = "temp_playlist.json"
NUMBER_OF_PLAYLISTS = 40
PLAYLIST_METADATA = 6

#Do a search of the playslists
def get_playlists(query, type, limit, market):

    spotify = spotipy.Spotify(requests_timeout=10, client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, ))

    valid_markets = ["AD","AE","AG","AL","AM","AO","AR","AT","AU","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BN","BO","BR","BS","BT","BW","BY","BZ","CA","CD","CG","CH","CI","CL","CM","CO","CR","CV","CW","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","ES","ET","FI","FJ","FM","FR","GA","GB","GD","GE","GH","GM","GN","GQ","GR","GT","GW","GY","HK","HN","HR","HT","HU","ID","IE","IL","IN","IQ","IS","IT","JM","JO","JP","KE","KG","KH","KI","KM","KN","KR","KW","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MG","MH","MK","ML","MN","MO","MR","MT","MU","MV","MW","MX","MY","MZ","NA","NE","NG","NI","NL","NO","NP","NR","NZ","OM","PA","PE","PG","PH","PK","PL","PS","PT","PW","PY","QA","RO","RS","RW","SA","SB","SC","SE","SG","SI","SK","SL","SM","SN","SR","ST","SV","SZ","TD","TG","TH","TJ","TL","TN","TO","TR","TT","TV","TW","TZ","UA","UG","US","UY","UZ","VC","VE","VN","VU","WS","XK","ZA","ZM","ZW"]

    if market in valid_markets:
        try:
            response = spotify.search(query, limit, 0, type, market)
            print(" has succeeded")
        except Exception as e:
            response = ""
            print(e)
            pass
    
    else:
        print("has no market support. Will try with no market.", end="")
        try:
            response = spotify.search(query, limit, 0, type)
            print(" {} has succeeded".format(query))
        except Exception as e:
            response = ""
            print(e)
            pass
     
    return response

#Get the playlists from a country
def request_playlist(country):
    
    type = "playlist"
    limit = NUMBER_OF_PLAYLISTS
        
    #Get country code for country. Needed for market search 
    try:
        codes = pycountry.countries.search_fuzzy(country)
        market = str(codes)[18] + str(codes)[19]
        print("{} {}".format(market, country), end="")
    except:
        print("   {} has no country code".format(country), end="")
        market = ""
    
    #Perform search
    playlists = get_playlists(country, type, limit, market)
    
    #Dump response in json file with all playlists found for country
    with open(OUTPUT_JSON, "w") as outfile:
        json.dump(playlists, outfile)

    return

#Process the response retrieved by Spotify
def go_through_response(country):

    #Substitute empty spaces with "-" so that map can access them properly
    country = country.replace(" ", "-")

    #open file where the playlist is for country X and load in JSON
    f = open(OUTPUT_JSON)

    #Initialize list of playlists for country X
    list_of_playlists=[None]*PLAYLIST_METADATA

    try:
        data = json.load(f)

        #See response format here: https://developer.spotify.com/console/get-search-item/
        for item in data['playlists']['items']:
            if 'external_urls' in item:
                urls = item["external_urls"]['spotify']
            if 'owner' in item:
                display_name = item["owner"]["display_name"]
            if 'name' in item:
                name= item["name"]

            #these are not obligatory, so should check if they are there
            if 'images' in item:
                try:
                    img = item["images"][0]['url']
                except:
                    img = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/01/AppleCompetition-FTRHeader_V1-1-300x171.png"
            if 'description' in item:
                try:
                    description =  item["description"] 
                except:
                    description = "No description"

            array = [country, urls, display_name, name, img, description]

            list_of_playlists = np.vstack((array, list_of_playlists))
            
        #List by name so that similalry named lists appear together (BROKEN)
        #list_of_playlists=np.sort(list_of_playlists, axis=1)
    
    except Exception as e:
        print(e)
        

    f.close()
    
    #repsonse from the country no longer needed, can tehrefore be deleted 
    if os.path.exists(OUTPUT_JSON):
        os.remove(OUTPUT_JSON)

    return list_of_playlists

#Fill in purpose
def fill_playlist_json(list_of_all_playlists):

    json_schema = {
        "countries": []
        }
    
    try:
        with open(TEMP_PLAYLIST_JSON, 'a') as json_file:
            for row in range(np.shape(list_of_all_playlists)[0]):
                country = {
                    "country": list_of_all_playlists[row, 0],
                    "playlists": [{
                        "link": list_of_all_playlists[row, 1],
                        "playlist_by": list_of_all_playlists[row, 2],
                        "name": list_of_all_playlists[row, 3],
                        "img": list_of_all_playlists[row, 4],
                        "description": list_of_all_playlists[row, 5]
                    }]
                }
                json_schema['countries'].append(country)
            json.dump(json_schema, json_file, indent=4, separators=(',', ': '))
    
    except Exception as e:
        print(e)

    return

def main():

    #Countries
    europe_countries = ["albania","andorra","austria","belarus","belgium","bosnia and herzegovina","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","san marino","italy","kosovo","latvia","liechtenstein","lithuania","luxembourg","macedonia","malta", "moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","russian federation","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","england", "isle of man", "northern ireland", "scotland", "wales"]
    
    list_of_all_playlists=[None]*PLAYLIST_METADATA

    for country in europe_countries:
        
        #Get the playlists from country X
        request_playlist(country)

        playlists = go_through_response(country)
        
        list_of_all_playlists = np.vstack((list_of_all_playlists, playlists))

        #Remove line of nones
        list_of_all_playlists = np.delete(list_of_all_playlists, (-1), axis=0)


    list_of_all_playlists = np.delete(list_of_all_playlists, (0), axis=0)
    #print(list_of_all_playlists)

    #fill the list with all the players
    fill_playlist_json(list_of_all_playlists)

    if os.path.exists(PLAYLIST_JSON):
        os.remove(PLAYLIST_JSON)

    if os.path.exists(TEMP_PLAYLIST_JSON):
        shutil.copyfile(TEMP_PLAYLIST_JSON, PLAYLIST_JSON)    
        os.remove(TEMP_PLAYLIST_JSON)
    
    
   


if __name__ == '__main__':
    main()
    