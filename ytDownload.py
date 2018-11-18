#!/usr/bin/env python

import sys
import pafy
import click
import threading
from concurrent.futures import ThreadPoolExecutor

@click.command()
@click.argument('urls', nargs=-1)
@click.option('-a', '--audio', is_flag=True)
def download(urls, audio):
    executor = ThreadPoolExecutor(max_workers=8)
    for url in urls:
        if 'playlist' in url:
            playlist = pafy.get_playlist(url)
            for item in playlist['items']:
                executor.submit(downloadBest, item['pafy'].videoid, audio)
        else:
            executor.submit(downloadBest, url, audio)
        
def downloadBest(url, audio):
    meta = pafy.new(url)
    file = meta.getbestaudio(preftype="m4a") if audio else meta.getbest()
    file.download()
    print("Finished: ", meta.title, "\t\t\t\t\t")
    
if __name__ == "__main__":
    download()
