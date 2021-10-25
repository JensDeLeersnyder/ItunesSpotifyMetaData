import re
# niet van toepassing artiesten worden toegevoegd door sidify en worden in het main programma geformateerd door gwn
# een / te zetten ipv een , met spaties

def main():
    artists = 'The Kid LAROI & Marshmello'
    trackName = "TRAGIC (feat. YoungBoy Never Broke Again & Internet Money & Marshmello"
    artist_list = re.split('& | ,', artists)

    # get all artists from the song title
    if "feat." in trackName:
        trackName_artists = re.split('& | , | feat.', trackName)
        trackName_artists[0] = (slicer(trackName_artists[0], "feat."))

        # add track name artist to arist list array
        for trackName_artist in trackName_artists:
            if trackName_artist not in artist_list:
                artist_list.append(trackName_artist.strip())

    song_metadata_artiest = ""
    for artiest in artist_list:
        song_metadata_artiest += artiest.strip()
        song_metadata_artiest += "/"
    song_metadata_artiest = song_metadata_artiest[0:len(song_metadata_artiest) - 1]
    print(song_metadata_artiest)


def slicer(my_str, sub):
    index = my_str.find(sub) + len(sub)
    if index != -1:
        return my_str[index:]
    else:
        raise Exception('Sub string not found!')


if __name__ == '__main__':
    main()
