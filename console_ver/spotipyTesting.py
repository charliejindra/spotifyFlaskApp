import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import random
from json.decoder import JSONDecodeError
from statMethods import *
from playlistMethods import *

# make playlist function
def makePlaylist():
    print("please enter a name for your playlist:")     
    playlistName = input()

    spotifyObj.trace = False

    #print ("range:", range)
    artistResults = spotifyObj.current_user_top_artists(time_range="medium_term", limit=50)
    #for i, item in enumerate(results['items']):
    #    print (i, item['name'])
    print

    
    artistsToGrab = []
    i = 0
    while i < 20:                                   # picks 20 random artists from your top 50
        #print(json.dumps(artistResults))
        
        #picks random artist from your top 50
        while True:
            goAhead = True # set it to false if theres a repeat
            newArtist = artistResults["items"][random.randint(0,48)]["id"]
            for artist in artistsToGrab:
                if newArtist == artist:
                    goAhead = False
                    break
            if goAhead == True:
                break
        
        artistsToGrab.append(newArtist)
        i = i + 1
    
    trackIds = []
    i = 0
    for artist in artistsToGrab:
        topTracks = spotifyObj.artist_top_tracks(artistsToGrab[i], country='US')
        #print(json.dumps(topTracks, indent=4))
        trackNo = random.randint(0,len(topTracks["tracks"])-1) # from 1 to the length of top tracks
        print(len(topTracks["tracks"]))
        print(str(trackNo) + "\n")
        trackIds.append(topTracks["tracks"][trackNo]["id"])
        tracksToUse = []
        tracksToUse.append(trackNo)

        #all of this is just a do while to make sure you check the new track against all other track #s of the artist
        while True:
            goAhead = True # set it to false if theres a repeat
            newTrack = random.randint(0,len(topTracks["tracks"])-1)
            for track in tracksToUse:
                if newTrack == track:
                    goAhead = False
                    break
            if goAhead == True:
                break
        trackIds.append(topTracks["tracks"][newTrack]["id"])
        tracksToUse.append(newTrack)
        
        #print(trackNo)
        i = i + 1

    spotifyObj.user_playlist_create(username, playlistName, public=True)     # make the playlist!!

    theId = ''
    playlists = spotifyObj.user_playlists(username, limit=1)
    print(json.dumps(playlists, indent=4))
    theId = playlists["items"][0]["id"]  # the 0th index is always the newest one created (right?)
    # for playlist in playlists:
    #     print(playlist)
    #     if (playlist["items"]["name"] == "twin spin"):

    print('done did the create')

    spotifyObj.user_playlist_add_tracks(username, theId, trackIds)
    
def statsMenu():
    while True:
        print('What sort of stats you want?')
        print('3 - Averages')
        print('2 - Top Artists')
        print('1 - Top Songs')
        print('0 - Exit')
        answer = input()
        if answer == "1":
            topSongs(spotifyObj)
        elif answer == "2":
            topArtists(spotifyObj)
        elif answer == "3":
            Averages(spotifyObj)
        elif answer == "0":
            break

def playlistMenu():
    while True:
        print('How would you like a playlist made?')
        print('2 - Twin Spin')
        print('1 - Reorder Existing')
        print('0 - Exit')
        answer = input()
        if answer == "1":
            reorderPlaylist(spotifyObj, username)
        elif answer == "2":
            twinSpin(spotifyObj, username)
        elif answer == "0":
            break

def getStats(trackId):
        
    track = spotifyObj.track(trackId)
    name = track["name"]
    artist = track["artists"][0]["name"]
    #print(json.dumps(track, indent=4))
    features = spotifyObj.audio_features(trackId)[0]
    #print(json.dumps(features, indent=4))

    print(name + " by " + artist)
    print("From album \"" + track["album"]["name"] + "\"")

    print("danceability     ", end="")
    printForStat(features["danceability"])
    print("energy           ", end="")
    printForStat(features["energy"])
    print("instrumentalness ", end="")
    printForStat(features["instrumentalness"])
    print("loudness         ", end="")
    printForStat((features["loudness"]+60)/60)
    print("mood             ", end="")
    printForStat(features["valence"])
    print("speed            ", end="")
    printForStat((features["tempo"]-50)/150)   
    
def printForStat(statAmt): #takes a 0.0 to 1.0 value and print bars to visualize value
    while statAmt > 0:
        print('|', end="")
        statAmt = statAmt - .05
    print("")
    
def searchMode():
    print('Type your track search here:')
    print('0 - Exit')
    answer = input()
    trackNo = 0       #search result number. can be incremented later
    while True:
        if answer == "0":
            break
        elif answer == "n":
            trackNo = trackNo + 1
        try:
            if not answer == "n": #reset to 1st result if new search
                trackNo = 0
                trackSearch = answer
            tracks = spotifyObj.search(trackSearch, limit=10, type="track")
            #print(json.dumps(tracks, indent=4))
            trackToAnalyze = tracks["tracks"]["items"][trackNo]["id"]
            print("-------------------------")
            getStats(trackToAnalyze)
        except:
            print("Your search found no results.")
        print("-------------------------")
        print("(n)ext - next search result")
        print("0 - Exit")
        print("Or enter another search result:")
        answer = input()

#get username and scope
username =  "charlessjindra"
# sys.argv[1]
scope = 'user-modify-playback-state user-top-read playlist-modify-public user-read-currently-playing playlist-read-collaborative'

#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope)
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#print('well we got past the stupid junk')
#set up spotify object
spotifyObj = spotipy.Spotify(auth=token)

while True:
    print('Welcome ' + username + '! Please select an option:')
    print('3 - Search for Song')
    print('2 - View Stats')
    print('1 - Playlist Creator')
    print('0 - Exit')
    answer = input()
    if answer == "1":
        playlistMenu()
    elif answer == "2":
        statsMenu()
    elif answer == "3":
        searchMode()
    elif answer == "0":
        break