#!/usr/bin/env python

import sys
import pafy
import threading
import argparse
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()
parser.add_argument('url', nargs='*')
parser.add_argument('-a', '--audio', action='store_true')

def download(urls=[], video=True):
    executor = ThreadPoolExecutor(max_workers=8)
    for url in urls:
        if 'playlist' in url:
            playlist = pafy.get_playlist(url)
            for item in playlist['items']:
                executor.submit(downloadBest, item['pafy'].videoid, video)
                #pool.apply_async(downloadBest, (item['pafy'].videoid, video))
                # threading.Thread(target=downloadBest, args=(item['pafy'].videoid, video)).start()
        else:
            executor.submit(downloadBest, url, video)
            #pool.apply_async(downloadBest, (url, video))
            # threading.Thread(target=downloadBest, args=(url, video)).start() 
        
def downloadBest(url, video=True):
    meta = pafy.new(url)
    if video: file = meta.getbest()
    else: file = meta.getbestaudio(preftype="m4a")
    file.download(quiet=True)
    print("Finished: ", meta.title, "\t\t\t\t\t")
    
if __name__ == "__main__":
    args = parser.parse_args()
    download(args.url, not args.audio)
