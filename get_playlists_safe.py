import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pycountry
import json
import numpy as np
import os
import shutil
import math

from configparser import ConfigParser
config=ConfigParser()
config.read('config.ini')
CLIENT_ID = config.get('keys', 'CLIENT_ID')
CLIENT_SECRET = config.get('keys', 'CLIENT_SECRET')

# Output JSON is where the response from spotify is temporarily stored and then removed 
OUTPUT_JSON = "test_output_playlists.json"
# Playlist.json file is where all the playlists are stored 
# temp is a temp file that then overwrites the other one
# Spotify playslists is where the playlists owned by spotify are
PLAYLIST_JSON = "playlist.json"
TEMP_PLAYLIST_JSON = "temp_playlist.json"
SPOTIFY_PLAYLISTS = "spotify_filtered_playlists.json"

# Number of playlists to query per country
NUMBER_OF_PLAYLISTS = 250

# Number of parameters to be kept
PLAYLIST_METADATA = 6

# List of EU countries and pruned list
EUROPE_COUNTRIES_OG = ["albania","andorra","austria","belarus","belgium","bosnia and herzegovina","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","san marino","italy","kosovo","latvia","liechtenstein","lithuania","luxembourg","macedonia","malta", "moldova","monaco","montenegro","netherlands","norway","poland","portugal","romania","russian federation","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","england", "isle of man", "northern ireland", "scotland", "wales"]
EUROPE_COUNTRIES = ["albania","andorra","austria","belarus","belgium","bosnia and herzegovina","bulgaria","croatia","cyprus","czech republic","denmark","estonia","france","finland","georgia","germany","greece","hungary","iceland","ireland","italy","kosovo","latvia","lithuania","luxembourg","macedonia","malta", "moldova","montenegro","netherlands","norway","poland","portugal","romania","russian federation","serbia","slovakia","slovenia","spain","sweden","switzerland","turkey","ukraine","england", "isle of man", "northern ireland", "scotland", "wales"]
TEST_COUNTRY = ["slovenia"]

######################################################################################################################

#Do a search of the playslists
def get_playlists(query, type, market, offset):

    spotify = spotipy.Spotify(requests_timeout=10, client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, ))

    valid_markets = ["AD","AE","AG","AL","AM","AO","AR","AT","AU","AZ","BA","BB","BD","BE","BF","BG","BH","BI","BJ","BN","BO","BR","BS","BT","BW","BY","BZ","CA","CD","CG","CH","CI","CL","CM","CO","CR","CV","CW","CY","CZ","DE","DJ","DK","DM","DO","DZ","EC","EE","EG","ES","ET","FI","FJ","FM","FR","GA","GB","GD","GE","GH","GM","GN","GQ","GR","GT","GW","GY","HK","HN","HR","HT","HU","ID","IE","IL","IN","IQ","IS","IT","JM","JO","JP","KE","KG","KH","KI","KM","KN","KR","KW","KZ","LA","LB","LC","LI","LK","LR","LS","LT","LU","LV","LY","MA","MC","MD","ME","MG","MH","MK","ML","MN","MO","MR","MT","MU","MV","MW","MX","MY","MZ","NA","NE","NG","NI","NL","NO","NP","NR","NZ","OM","PA","PE","PG","PH","PK","PL","PS","PT","PW","PY","QA","RO","RS","RW","SA","SB","SC","SE","SG","SI","SK","SL","SM","SN","SR","ST","SV","SZ","TD","TG","TH","TJ","TL","TN","TO","TR","TT","TV","TW","TZ","UA","UG","US","UY","UZ","VC","VE","VN","VU","WS","XK","ZA","ZM","ZW"]

    query = get_country_search_term(query)

    if market in valid_markets:
        try:
            response = spotify.search(query, 50, offset*50, type, market)
            print(" has succeeded. Search number {}".format(offset+1))
        except Exception as e:
            response = ""
            print(e)
            pass
    
    else:
        print(" This country had no market support. Will try with no market.", end="")
        try:
            response = spotify.search(query, 50, offset*50, type)
            print(" {} has succeeded. Search number {}".format(query, offset+1))
        except Exception as e:
            response = ""
            print(e)
            pass
     
    return response

#Get the playlists from a country
def request_playlist(country, offset):
    
    type = "playlist"
        
    #Get country code for country. Needed for market search 
    try:
        codes = pycountry.countries.search_fuzzy(country)
        market = str(codes)[18] + str(codes)[19]
        print("{} {}".format(market, country), end="")
    except:
        print("   {} has no country code.".format(country), end="")
        market = ""
    
    #Perform search
    playlists = get_playlists(country, type, market, offset)

    #Dump response in json file with all playlists found for country
    
    with open(OUTPUT_JSON, "w") as outfile:
        json.dump(playlists, outfile)

    return

#Process the response retrieved by Spotify
def process_response(country):

    #Substitute empty spaces with "-" so that map can access them properly
    country = country.replace(" ", "-")

    #open file where the playlist is for country X and load in JSON
    f = open(OUTPUT_JSON)

    #Initialize list of playlists for country X
    list_of_playlists=[]

    try:
        data = json.load(f)

        #See response format here: https://developer.spotify.com/console/get-search-item/
        for item in data['playlists']['items']:
            if item:
                if 'external_urls' in item:
                    urls = item["external_urls"]['spotify']
                if 'owner' in item:
                    display_name = item["owner"]["display_name"]
                if 'name' in item:
                    name= item["name"]
                    

                #Not obligatory, so should check if it is there
                if 'images' in item:
                    try:
                        img = item["images"][0]['url']
                    except:
                        img = "https://storage.googleapis.com/pr-newsroom-wp/1/2023/01/AppleCompetition-FTRHeader_V1-1-300x171.png"
                
                if 'description' in item:
                    description =  item["description"]
                    if description == "":
                        description = "No description"


                array = [country, urls, display_name, name, img, description]
                list_of_playlists.append(array)

    except Exception as e:
        print(e) 

    f.close()
    
    #Response from the country no longer needed, can therefore be deleted 
    if os.path.exists(OUTPUT_JSON):
        os.remove(OUTPUT_JSON)

    return list_of_playlists

#Fill in purpose
def fill_playlist_json(list_of_all_playlists):

    json_schema = {
        "countries": []
        }
    

    #List by name so that similalry named lists appear together
    list_of_all_playlists = list(filter(lambda x: np.any(x), list_of_all_playlists))
    list_of_all_playlists = np.array(list_of_all_playlists,dtype=object)
    try:
        indices = np.argsort(list_of_all_playlists[:,3])
        list_of_all_playlists = list_of_all_playlists[indices]
    except Exception as e:
        print(e)

    #Write to the final JSON file
    try:
        with open(TEMP_PLAYLIST_JSON, 'a') as json_file:
            for row in range(np.shape(list_of_all_playlists)[0]):
                #Remove all "This is" playlists 
                if "This Is" not in list_of_all_playlists[row, 3]:
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

# Spotify breaking balls and not showing their own playlists anymore. Add from previous queries
def add_spotify_playlists():
    
    with open(SPOTIFY_PLAYLISTS, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with open(PLAYLIST_JSON, 'r', encoding='utf-8') as file:
        data2 = json.load(file)

    # Get the relevant playlists
    countries = data.get("countries", [])

    if "countries" not in data2:
        data2['countries'].append(data)
    
    data2["countries"].extend(countries)

    #reverse the data so spotify playlists are on top
    data2["countries"] = data2["countries"][::-1]

    with open(PLAYLIST_JSON, 'w', encoding='utf-8') as file:
        json.dump(data2, file, indent=4, ensure_ascii=False)

    return

# Generate a serach query for each country - includes alternative names for countries
def get_country_search_term(country):

    europe_countries_search_term = ["albania","andorra","osterreich austria","belarus","belgium","bosnia and herzegovina","bulgaria","croatia hrvatska","cyprus","czech republic","denmark dansk","estonia","france","finland","georgia","germany","greece Ελληνική","hungary magyar","iceland island","ireland","italia","kosovo","latvia","lithuania","luxembourg","macedonia","malta", "moldova","montenegro","netherlands","norway norske","poland polskie","portugal","romania","russia","serbia","slovakia","slovenia","espana","sweden svensk","switzerland","turkey","ukraine","england", "isle of man", "northern ireland", "scotland", "wales"]
 
    name = europe_countries_search_term[EUROPE_COUNTRIES.index(country)]

    return name

def main():

    #Countries
    europe_countries = EUROPE_COUNTRIES
    
    list_of_all_playlists = [None]*PLAYLIST_METADATA
    number_of_searches = math.ceil(NUMBER_OF_PLAYLISTS / 50)

    for country in europe_countries:    
        for offset in range(number_of_searches):
            
            #Get the playlists from country X with offset
            request_playlist(country, offset)

            batch_of_playlists = process_response(country)
            
            if (batch_of_playlists):
                try:
                    list_of_all_playlists = np.vstack((list_of_all_playlists, batch_of_playlists))
                except Exception as e:
                    print(e)


    # Fill the list with all the playlists
    fill_playlist_json(list_of_all_playlists)


    if os.path.exists(TEMP_PLAYLIST_JSON):
        shutil.copyfile(TEMP_PLAYLIST_JSON, PLAYLIST_JSON)    
        os.remove(TEMP_PLAYLIST_JSON)
    
    add_spotify_playlists()



if __name__ == '__main__':
    main()
    