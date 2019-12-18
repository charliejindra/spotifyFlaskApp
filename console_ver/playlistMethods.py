import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import random
from json.decoder import JSONDecodeError

def reorderPlaylist(spotifyObj, username):
    playlists = spotifyObj.current_user_playlists(limit=50)
    #print(json.dumps(playlists, indent=4))
    print("+-------------------+")
    print("Please select the playlist you'd like to reorder:")
    for i, playlist in enumerate(playlists['items']):
        print("{} {}".format(i+1, playlist['name']))
    print("+-------------------+")
    answer = input()
    playlistIndex = int(answer) - 1     # the minus 1 is to turn rank into index number
    playlistToReorder = playlists['items'][playlistIndex]['id']
    #print(json.dumps(playlistToReorder, indent=4))
    actualPlaylistToReorder = spotifyObj.user_playlist(username, playlistToReorder)
    print(json.dumps(actualPlaylistToReorder, indent=4))
    oldTracks = actualPlaylistToReorder['tracks']['items']
    print(len(oldTracks))
    

    while True:
        print('Please select an ordering scheme:')
        print('4 - instrumentals - least to most')
        print('3 - tempo: slowest to fastest')
        print('2 - valence: saddest to happiest')
        print('1 - energy: calmest to wildest')
        answer = input()

        quantifier = ""
        loToHigh = True

        if answer == "1":
            quantifier = "tempo"
            loToHigh = True
            break
        elif answer == "2":
            quantifier = "valence"
            loToHigh = True
            break
        elif answer == "3":
            quantifier = "energy"
            loToHigh = True
            break
        elif answer == "4":
            quantifier = "instrumentalness"
            loToHigh = True
            break

    print("please enter a name for your playlist:")
    playlistName = input()
    
    infoList = []
    for item in enumerate(oldTracks):
            #print(json.dumps(item[1], indent=4))
            infoList.append(item[1]['track']['id'])
            i = i + 1

        #print('ok were out of the woods')
        
    #print(json.dumps(results['items'][0], indent=4))
    tracksFeatures = []
    tracksFeatures = tracksFeatures + spotifyObj.audio_features(infoList)

    # create dictionary of songs for sorting
    #print(json.dumps(tracksFeatures, indent=4))
    arrayOfSongs = []
    for song in tracksFeatures:
        print(json.dumps(song, indent=4))
        arrayOfSongs.append([song['id'],song[quantifier]])

    print(arrayOfSongs)

    swapped = True
    while swapped:
        swapped = False
        for i in range(len(arrayOfSongs) - 1):
            if arrayOfSongs[i][1] > arrayOfSongs[i + 1][1]:
                # Swap the elements
                arrayOfSongs[i], arrayOfSongs[i + 1] = arrayOfSongs[i + 1], arrayOfSongs[i]
                # Set the flag to True so we'll loop again
                swapped = True

    print(arrayOfSongs)

    

    spotifyObj.user_playlist_create(username, playlistName, public=True)     # make the playlist!!

    trackIds = []
    for track in arrayOfSongs:
        #print(json.dumps(track, indent=4))
        trackIds.append(track[0])

    print(trackIds)

    playlists = spotifyObj.current_user_playlists(limit=20) #refresh so that the new playlist is there

    theId = playlists["items"][0]["id"]  # the 0th index is always the newest one created (right?)

    
    spotifyObj.user_playlist_add_tracks(username, theId, trackIds)

    return

def twinSpin(spotifyObj, username):
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
        #print(len(topTracks["tracks"]))
        #print(str(trackNo) + "\n")
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
    
    print(username)
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