import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def getSpotifyArtists(search_string):
    mode = "a"
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="",
                                                               client_secret="",
                                                               ))
    results = sp.search(q='tragoc the kid laroi', limit=20)

    if mode == "m":
        for idx, track in enumerate(results['tracks']['items']):
            print(idx, track['name'])
            number = input("number:")
            artists = results.get("tracks").get("items")[number].get("artists")
    else:
        artists = results.get("tracks").get("items")[0].get("artists")

    artist_list = []
    for artist in artists:
        artist_list.append(artist.get("name"))

    return artist_list

if __name__ == '__main__':
    main()
