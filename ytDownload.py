import sys
import pafy
import threading
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='*')
parser.add_argument('-a', '--audio', action='store_true')

def download(urls=[], video=True):
    for url in urls:
        if 'playlist' in url:
            playlist = pafy.get_playlist(url)
            for item in playlist['items']:
                threading.Thread(target=downloadBest, args=(item['pafy'].videoid, video)).start()
        else:
            threading.Thread(target=downloadBest, args=(url, video)).start() 
        
def downloadBest(url, video=True):
    meta = pafy.new(url)
    if video: file = meta.getbest()
    else: file = meta.getbestaudio(preftype="m4a")
    file.download()
    print("Finished: ", meta.title, "                                                               ")
    
if __name__ == "__main__":
    args = parser.parse_args()
    download(args.url, not args.audio)