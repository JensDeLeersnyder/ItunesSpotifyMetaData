import eyed3
from pathlib import Path
from glob import glob
import itunespy


def main():
    directory = r"{}".format(input(
        "Geef het pad in voor de folder waar je de tags wilt veranderen druk 0 in voor te stoppen: "))
    while directory != 0:
        song_paths = get_song_path(directory)
        format_artist_list(song_paths)
        directory = r"{}".format(input(
            "Geef het pad in voor de folder waar je de tags wilt veranderen druk 0 in voor te stoppen: "))


def get_song_path(directory):
    song_path_list = ''
    underlying_folder_yes_or_no = input(
        "geef \"True\" of \"False\" in als er onderliggende folders zijn: ")
    underlying_folder_yes_or_no = underlying_folder_yes_or_no.lower()
    while underlying_folder_yes_or_no != "true" and underlying_folder_yes_or_no != "false":
        print("Foute input")
        underlying_folder_yes_or_no = input(
            "geef \"True\" of \"False\" in als er onderliggende folders zijn: ")

    if underlying_folder_yes_or_no == "true":
        sub_directory_list = glob(directory + "\\*\\")
        for subdirectoryPath in sub_directory_list:
            song_path_list = list(Path(subdirectoryPath).glob('**/*.mp3'))
    else:
        song_path_list = list(Path(directory).glob('**/*.mp3'))

    return song_path_list


# this program will split the artist and add a '/' between artist
def format_artist_list(song_path_list):
    for song_path in song_path_list:
        audio_file = eyed3.load(r"{}".format(song_path))
        artist_not_formatted = audio_file.tag.artist
        artist_list = artist_not_formatted .split(',')

        song_metadata_artiest = ""
        for artiest in artist_list:
            song_metadata_artiest += artiest.strip()
            song_metadata_artiest += "/"
        song_metadata_artiest = song_metadata_artiest[0:len(
            song_metadata_artiest) - 1]
        print(song_metadata_artiest)
        audio_file.tag.artist = song_metadata_artiest
        audio_file.tag.save()


def get_song_information_from_itunes():
    print('true')


if __name__ == '__main__':
    main()
