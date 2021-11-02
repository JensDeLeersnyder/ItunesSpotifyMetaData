import requests
import applemusicspy


def main():
    # id_number = "1440834528"
    id_number = "1440842746"
    # response_class = applemusicspy.lookup(id="1577439449")
    # print(response_class)

    track_info = applemusicspy.lookup(itunesID=id_number, trackName="Broken+Arrows", albumArtist="Avicii")
    album_info = applemusicspy.lookup(itunesID=track_info[0].get("collectionId"), trackName="Broken+Arrows", albumArtist="Avicii")

    SongInformationDictionary = {
                                 'trackName': track_info[0].get("trackName"),
                                 'albumName': track_info[0].get("collectionName"),
                                 'releaseDate': track_info[0].get("releaseDate"),
                                 'trackNumber': track_info[0].get("trackNumber"),
                                 'genre': album_info[0].get("primaryGenreName"),
                                 'albumArtist': track_info[0].get("artistName")
                                 }

    print(SongInformationDictionary)

if __name__ == '__main__':
    main()
