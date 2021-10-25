import itunespy


def main():
    id_number = '1440842746'
    #id_number = '1578326262'

    track_info = itunespy.lookup(id=id_number)
    album_info = itunespy.lookup(id=track_info[0].collectionId)

    track = itunespy.search_track('arrows')
    print(track[0].artist_name + ': ' + track[0].track_name + ' | Length: ' + str(
        track[0].get_track_time_minutes()))  # Get info from the first result

if __name__ == '__main__':
    main()
