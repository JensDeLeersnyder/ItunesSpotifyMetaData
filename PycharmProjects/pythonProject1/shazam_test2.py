import asyncio
from shazamio import Shazam


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(shazamInformation())

async def shazamInformation(song_path):
    shazam = Shazam()
    out = await shazam.recognize_song(song_path)
    itunesId = out.get("track").get("hub").get("actions")[0].get("id")
    spotifySearchStringNotFormatted = out.get("track").get("hub").get("providers")[0].get("actions")[0].get("uri")

    spotifySearchString = spotifySearchStringNotFormatted.split("%20")
    spotifySearchString[0] = spotifySearchString[0].split(":")[2]


if __name__ == '__main__':
    main()









