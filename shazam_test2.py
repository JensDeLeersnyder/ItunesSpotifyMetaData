import asyncio
from shazamio import Shazam

async def main():
    shazam = Shazam()
    out = await shazam.recognize_song(
        r'C:\Users\gamerjens\Desktop\Script Music\test\TRAGIC (feat. Youngboy Never Broke Again & Internet Money)  - '
        r'The Kid LAROI, YoungBoy Never Broke Ag.mp3')
    print(out)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
