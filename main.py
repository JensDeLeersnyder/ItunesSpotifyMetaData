import eyed3
from pathlib import Path
from glob import glob
import applemusicspy
import datetime
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import asyncio
from shazamio import Shazam
import urllib.request
import os
import re
from mutagen.easyid3 import EasyID3
import shutil
import configparser

def main():
    print("Artist metadata and albumart is provided by Spotify") 
    directory = r"{}".format(input(
        "Geef het pad in voor de folder waar je de tags wilt veranderen druk 0 in voor te stoppen: "))
    if directory == 0:
        exit()
    mode = input("[A]utomatic or [M]anual: ").lower()
    while mode != "a" and mode != "m":
        print("Foute Input")
        mode = input("[A]utomatic or [M]anual: ").lower()

    songSource = input("Song source: [S]potify [O]ther: ").lower()
    while songSource != "s" and songSource != "o":
        print("Foute Input")
        songSource = input("Song source: [S]potify [O]ther: ").lower()

    song_paths_list = get_song_paths(directory)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(shazamInformation(song_paths_list, mode, songSource, directory))


def get_song_paths(directory):
    song_path_list = ''
    underlying_folder_yes_or_no = input(
        "geef \"True\" of \"False\" in als er onderliggende folders zijn: ")
    underlying_folder_yes_or_no = underlying_folder_yes_or_no.lower()
    while underlying_folder_yes_or_no != "true" and underlying_folder_yes_or_no != "false":
        print("Foute input")
        underlying_folder_yes_or_no = input(
            "geef \"True\" of \"False\" in als er onderliggende folders zijn: ")
    print("-----------------------------------------------------------")
    song_path_list = []
    if underlying_folder_yes_or_no == "true":
        sub_directory_list = glob(directory + "\\*\\")
        for subdirectoryPath in sub_directory_list:
            song_path_list += list(Path(subdirectoryPath).glob('**/*.mp3'))
    else:
        song_path_list = list(Path(directory).glob('./*.mp3'))

    return song_path_list


# this program will split the artist and add a '/' between artist
def format_artist_list(artists, mode):
    artist_list = artists.split(',')

    song_metadata_artiest = ""
    for artiest in artist_list:
        song_metadata_artiest += artiest.strip()
        song_metadata_artiest += "/"
    song_metadata_artiest = song_metadata_artiest[0:len(
        song_metadata_artiest) - 1]
    return song_metadata_artiest


def formatdate(releaseDate):
    date = datetime.datetime.strptime(releaseDate, "%Y-%m-%dT%H:%M:%SZ")
    belgiumFormat = "%d/%m/%Y"
    return date.strftime(belgiumFormat)


def get_song_information_from_itunes(id_number, trackName, albumArtist):
    track_info = applemusicspy.lookup(itunesID=id_number, trackName=trackName, albumArtist=albumArtist)
    album_info = applemusicspy.lookup(itunesID=track_info[0].get("collectionId"), trackName=trackName,
                                      albumArtist=albumArtist)

    SongInformationDictionary = {'trackName': track_info[0].get("trackName"),
                                 'albumName': track_info[0].get("collectionName"),
                                 'releaseDate': track_info[0].get("releaseDate"),
                                 'trackNumber': track_info[0].get("trackNumber"),
                                 'genre': album_info[0].get("primaryGenreName"),
                                 'albumArtist': track_info[0].get("artistName")}
    return SongInformationDictionary


def saveImageFromInternet(urls, albumName):
    biggestImageUrl = ""
    biggestImageSize = 0
    for url in urls:
        if url.get("width") > biggestImageSize:
            biggestImageUrl = url.get("url")
            biggestImageSize = url.get("width")

    current_directory = os.getcwd()
    saveDirectory = os.path.join(current_directory, "AlbumArtImages")
    if not os.path.exists(saveDirectory):
        os.mkdir(saveDirectory)

    imageSavePlace = os.path.join(saveDirectory, biggestImageUrl.split('/')[len(biggestImageUrl.split('/')) - 1]) + "png"

    urllib.request.urlretrieve(biggestImageUrl, imageSavePlace)

    return imageSavePlace


def getSpotifyArtistsAndAlbumArtURL(search_string, mode):
    # Read in config from config.cfg file
    config = configparser.ConfigParser()
    config.read('config.cfg')

    # catch error if cant find song on spotify
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=config['Spotify']["client_id"],
                                                               client_secret=config['Spotify']["client_secret"]))

    results = sp.search(q=search_string, limit=20)
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

    imageSources = results.get("tracks").get("items")[0].get("album").get("images")
    albumNameFromSpotify = results.get("tracks").get("items")[0].get("album").get("name")
    imagePath = saveImageFromInternet(imageSources, albumNameFromSpotify)
    url = results.get("tracks").get("items")[0].get("external_urls").get("spotify")

    spotifyInformation = {'artists': artist_list, 'imagePath': imagePath, 'SpotifyURL': url}
    return spotifyInformation

def movetofailed(headPath, song_path):
    failed_directory = headPath + "\\failed"
    if not os.path.exists(failed_directory):
        os.mkdir(failed_directory)
    shutil.move(song_path, failed_directory + "\\{}".format(song_path.name))
    print("{} was moved to failed".format(song_path.name))
    print("-----------------------------------------------------------")

async def shazamInformation(song_paths, mode, songSource, headPath):
    for song_path in song_paths:
        shazam = Shazam()
        out = await shazam.recognize_song(song_path)
        if out.get("track") is None:
            movetofailed(headPath, song_path)
        else:
            try:
                itunesId = out.get("track").get("hub").get("actions")[0].get("id")
                trackname = out.get("track").get("urlparams").get("{tracktitle}")
                albumArtist = out.get("track").get("urlparams").get("{trackartist}")
                ItunesInformationDictionary = get_song_information_from_itunes(itunesId, trackname, albumArtist)
            
                if songSource == "o":
                    spotifySearchStringNotFormatted = out.get("track").get("hub").get("providers")[0].get("actions")[0].get(
                        "uri")

                    spotifySearchList = spotifySearchStringNotFormatted.split("%")
                    spotifySearchList[0] = spotifySearchList[0].split(":")[2]

                    spotifySearchString = ""
                    for spotifySearchPart in spotifySearchList:
                        spotifySearchString += spotifySearchPart + " "
                    spotifySearchString = re.sub('[0-9]', '', spotifySearchString.strip())

                    spotifyInformation = getSpotifyArtistsAndAlbumArtURL(spotifySearchString, mode)

                    artists = ""
                    for oneArtist in spotifyInformation.get("artists"):
                        artists += oneArtist + ","
                    artists = artists[0:len(artists) - 1]

                    allSongInformation = {
                        'imageDirectory': spotifyInformation.get("imagePath"),
                        'SpotifyURL': spotifyInformation.get("SpotifyURL")
                    }
                else:
                    audio_file = eyed3.load(r"{}".format(song_path))
                    artists = audio_file.tag.artist

                allSongInformation = {'song_path': song_path,
                                      'headPath': headPath,
                                      'trackName': ItunesInformationDictionary.get("trackName"),
                                      'artists': artists,
                                      'albumName': ItunesInformationDictionary.get("albumName"),
                                      'releaseDate': ItunesInformationDictionary.get("releaseDate"),
                                      'trackNumber': ItunesInformationDictionary.get("trackNumber"),
                                      'genre': ItunesInformationDictionary.get("genre"),
                                      'albumArtist': ItunesInformationDictionary.get("albumArtist")
                                      }
                add_information_to_song(allSongInformation, mode)
            except (IndexError, TypeError):
                movetofailed(headPath, song_path)



def initiateTags(song_path):
    audio_file = eyed3.load(r"{}".format(song_path))

    if audio_file.tag is None:
        audio_file.initTag()
    audio_file.tag.save()


def add_information_to_song(songInformation, mode):
    releaseDate = formatdate(songInformation.get("releaseDate"))
    releaseYear = releaseDate.split("/")[2]
    artists = format_artist_list(songInformation.get("artists"), mode)

    initiateTags(songInformation.get("song_path"))

    try:
        audio_file = eyed3.load(r"{}".format(songInformation.get("song_path")))
        audio_file.tag.title = songInformation.get("trackName")
        audio_file.tag.artist = artists
        audio_file.tag.album = songInformation.get("albumName")
        audio_file.tag.BestDate = releaseYear
        audio_file.tag.track_num = songInformation.get("trackNumber")
        audio_file.tag.genre = songInformation.get("genre")
        audio_file.tag.album_artist = songInformation.get("albumArtist")

        if mode == "o":
            with open(songInformation.get("imageDirectory", "rb"), "rb") as cover_art:
                audio_file.tag.images.set(0, cover_art.read(), "image/jpeg")

        audio = EasyID3(songInformation.get("song_path"))
        audio["date"] = releaseYear
        audio.save()

        print("Name: {} \n"
              "Artists: {} \n"
              "Album: {} \n"
              "ReleaseYear: {} \n"
              "Nr: {} \n"
              "Genre: {} \n"
              "AlbumArtist: {} \n"
              "Spotify: {} \n"
              "-----------------------------------------------------------".format(songInformation.get("trackName"),
                                                                                   artists,
                                                                                   songInformation.get("albumName"),
                                                                                   releaseYear,
                                                                                   songInformation.get("trackNumber"),
                                                                                   songInformation.get("genre"),
                                                                                   songInformation.get("albumArtist"),
                                                                                   songInformation.get("SpotifyURL")))
        audio_file.tag.save()
    except EasyID3.id3:
        movetofailed(songInformation.get("headPath"), songInformation.get("song_path"))


if __name__ == '__main__':
    main()
