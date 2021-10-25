import itunespy


def main():
    #working song
    #broken arrows avici https://music.apple.com/us/album/stories/1440834059
    #id_number = '1440834528'

    #tragic the kid laroy https://music.apple.com/gb/album/tragic-feat-youngboy-never-broke-again-internet-money/1538646756?i=1538647031
    id_number = '1538647031'
    #actiall id he looks up

    track_info = itunespy.lookup(id=id_number)
    album_info = itunespy.lookup(id=track_info[0].collectionId)

    track = itunespy.search_track('arrows')
    print(track[0].artist_name + ': ' + track[0].track_name + ' | Length: ' + str(
        track[0].get_track_time_minutes()))  # Get info from the first result

if __name__ == '__main__':
    main()
