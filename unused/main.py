from GenerateArtists import generate_artist_list
from SortingAlgorithms import mergeSort, quickSortIt
from SimlarityAlgo import get_similarity_score
from time import sleep
from random import randint, shuffle
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import unused.ascii as ascii


#retrieve spotify api credentials
client_id = '024d2accff6645c7919e60466b8ec3f0'
client_secret = '2ed4211bd77444bf8f04f87508c4073c'

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#load welcome message
ascii.welcome()
sleep(2)
ascii.loadingIP()

#prompt user for genre
genre=""
while (genre !="data.json" and genre!="metal.json" and genre!="hip-hop.json" and genre!="indie.json" and genre!="pop.json" and genre!="rap.json" and genre!="rock.json"):
    print("Select one of the following datasets: ")
    print("\ndata.json, metal.json, hip-hop.json, indie.json, pop.json, rap.json, rock.json\n")
    genre = input("Your Choice: ")

#load json file
with open("./data/" + genre) as file:
    artist_list = json.load(file)
artist_list = generate_artist_list(artist_list)
ascii.loadingComplete()

#organize data
sortingAlg = ""
while sortingAlg != '1' and sortingAlg != '2':

    sortingAlg = input("choose 1 for quicksort and 2 for mergesort: ")

    match sortingAlg:
        case "1":
            quickSortIt(artist_list, 0, len(artist_list)-1)
        case "2": 
            mergeSort(artist_list, 0, len(artist_list)-1)


#begin game mechanics
score = 0
level = 0
has_lost = False
current_index = len(artist_list) - randint(1,30)
while (not has_lost):

    #current artist must have related artists
    current_artist = artist_list[current_index]
    related_artists = sp.artist_related_artists(current_artist.get_id())['artists']
    if not related_artists:
        current_index -= 1
        continue

    #get related artists name and id
    related_artist = {
    'name': related_artists[randint(0, len(related_artists) - 1)]['name'],
    'id': related_artists[randint(0, len(related_artists) - 1)]['id']
    }

    #get non-related artists name and id
    nearby_index = current_index + randint(1, 10)
    while nearby_index < 0 or nearby_index >= len(artist_list) or nearby_index == current_index:
        nearby_index = current_index - randint(1, 10)
    nearby_artist = {
    'name': artist_list[nearby_index].get_name(),
    'id': artist_list[nearby_index].get_id()
    }

    #shuffle options
    options = [related_artist, nearby_artist]
    shuffle(options)

    #display options to user
    print(f'\nLEVEL : {level}\n\nNAME OF ARTIST : {current_artist.get_name()}\n')
    print(f'Who do {current_artist.get_name()} fan''s listen to more?\n')
    
    option1_score = get_similarity_score(current_artist.get_id(), options[0]['id'])
    option2_score = get_similarity_score(current_artist.get_id(), options[1]['id'])
    
    if option1_score > option2_score:
        correct_option = "1"
        print("Option 1: " + options[0]['name'])
        print("Option 2: " + options[1]['name'])
    else:
        correct_option = "2"
        print("Option 1: " + options[1]['name'])
        print("Option 2: " + options[0]['name'])
    user_input = input("\ntype 1 for option 1 and 2 for option 2: ")
    if (user_input == correct_option):
        score += 1
        level += 1
        current_index -=  randint(1, 30)
        print("\n--------------------------CORRECT!---------------------------")
    else:
        has_lost = True
        print("\nyou lost! Your final score: " + str(score))