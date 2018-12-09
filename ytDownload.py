#!/usr/bin/env python

from concurrent.futures import ThreadPoolExecutor
import pafy
import click

@click.command()
@click.argument('urls', nargs=-1)
@click.option('-a', '--audio', is_flag=True)
@click.option('-ps', '--pstart', type=int, default = 1)
@click.option('-pe', '--pend', type=int, default=10000)
def download(urls, audio, pstart, pend):
    """Calls download_best for each video url."""
    executor = ThreadPoolExecutor(max_workers=8)
    for url in urls:
        if 'playlist' in url:
            playlist = pafy.get_playlist(url)
            end = min(pend, len(playlist['items']))
            for item in playlist['items'][pstart-1:end]:
                executor.submit(download_best, item['pafy'], audio)
        else:
            executor.submit(download_best, pafy.new(url), audio)

def download_best(meta, audio):
    """Download the specified video/audio."""
    file = meta.getbestaudio(preftype="m4a") if audio else meta.getbest()
    file.download()
    print("Finished: ", meta.title, "\t\t\t\t\t")

if __name__ == "__main__":
    download()
