import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import random
from json.decoder import JSONDecodeError

def topArtists(spotifyObj):
    ranges = ["short_term", "medium_term", "long_term"]
    for range in ranges:
        print(range)
        print('+------------------------------------------+')
        results = spotifyObj.current_user_top_artists(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            print ("|", i, item['name'])
        print('+------------------------------------------+\n\n')
    print

def topSongs(spotifyObj):
    ranges = ["short_term", "medium_term", "long_term"]
    for range in ranges:
        print(range)
        print('+------------------------------------------+')
        results = spotifyObj.current_user_top_tracks(time_range=range, limit=50)
        for i, item in enumerate(results['items']):
            print ("|", i, item['name'])
        print('+------------------------------------------+\n\n')
    print

def Averages(spotifyObj):
    amount = 0

    tempoTotal = 0
    danceTotal = 0
    energyTotal = 0
    loudnessTotal = 0
    speechinessTotal = 0
    acousticnessTotal = 0
    instrumentTotal = 0
    livenessTotal = 0
    valenceTotal = 0

    ranges = ["short_term", "medium_term", "long_term"]
    for range in ranges:
        print('Getting {} data...\n\n'.format(range))
        results = spotifyObj.current_user_top_tracks(time_range=range, limit=50)

        #add all the track ids to one place so we can make one api call for all the features
        resultsList = []
        #print(json.dumps(results['items'][0], indent=4))
        i = 0
        #print(len(results['items']))
        for item in enumerate(results['items']):
            #print(item[1]['id'])
            resultsList.append(item[1]['id'])
            i = i + 1

        #print('ok were out of the woods')
        
        #print(json.dumps(results['items'][0], indent=4))
        features = spotifyObj.audio_features(resultsList)

        for item in enumerate(features):
            #print(item[i]['tempo'])
            #print(json.dumps(features, indent=4))
            
            danceTotal = danceTotal + item[1]['danceability']
            energyTotal = energyTotal + item[1]['energy']
            loudnessTotal = loudnessTotal + item[1]['loudness']
            speechinessTotal = speechinessTotal + item[1]['acousticness']
            instrumentTotal = instrumentTotal + item[1]['instrumentalness']
            livenessTotal = livenessTotal + item[1]['liveness']
            valenceTotal = valenceTotal + item[1]['valence']
            tempoTotal = tempoTotal + item[1]['tempo'] # index 0 bc its a list of features of length 1

            # print(tempoTotal)
            amount = amount + 1
    print(amount)
    avgFeatures = {
            "danceability": danceTotal / amount,
            "energy": energyTotal / amount,
            "loudness": loudnessTotal / amount,
            "speechiness": speechinessTotal / amount,
            "acousticness": acousticnessTotal / amount,
            "instrumentalness": instrumentTotal / amount,
            "liveness": livenessTotal / amount,
            "valence": valenceTotal / amount,
            "tempo": tempoTotal / amount
        }

    print(json.dumps(avgFeatures, indent=4))