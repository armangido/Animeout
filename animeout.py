from main import Animeout
import requests
import os
from tqdm import tqdm
from pathlib import Path
import threading
import tempfile
import time

kill_threads = False

def scrape_direct(url,json=False):
    links = Animeout()._scrape_ddl(url)
    if json == True:
        links = json.dumps(links)
    qualities = [quality for quality in links.keys()]
    while True:
        quality = input(f'What quality you want? {qualities}: ')
        try:
            print(f'{len(links[quality])} Download links')
            return links[quality]
        except KeyError:
            print('Quality not found try again')
            time.sleep(2)
            continue

def scrape_mega(url,json=False):
    links = Animeout()._scrape_mega(url)
    if json == True:
        links = json.dumps(links)
    return links

def downloads(urls,threads=2,directory=None,interval=120):
    for url in urls:
        download(url,threads=threads,directory=directory)

def download(url,threads=None,directory=None):
    if directory is not None and os.path.exists(directory):
        print(f'Changing Directory from {os.getcwd()} at {directory}')
        os.chdir(directory)
    url = requests.get(url).url.split('=')[1]
    location = requests.get(f'http://public.animeout.xyz/{url}',allow_redirects=False).headers['Location']
    filesize = int(requests.head(location).headers['Content-Length'])
    filename = requests.utils.unquote(os.path.basename(url))
    print(f'Downloading {filename}...')
    if threads is None:
       try:
        req = requests.get(location,stream=True)
        with open(filename,'wb+') as f,tqdm(
                unit='B',
                desc=filename,
                total=filesize,
                unit_scale=True
            ) as bar:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(1024)
       except KeyboardInterrupt:
           print(f'Download {filename} has been cancelled, removing file!!!')
           if os.path.exists(filename):
                os.remove(filename)
    else:
        print(f'Downloading {filename} using {threads} thread(s)')
        _download_file(location,filename,filesize,threads=threads)
def _handle_thread(thread_lists):
    while True:
        if kill_threads == True:
            thread_lists.clear()
        for thread in thread_lists:
            if not thread.is_alive():
                thread_lists.remove(thread)
            else:
                continue
        if not thread_lists:
            return True
def _merge_(directory,filename):
    files = os.listdir(directory).sort()
    with open(filename,'wb+')as output:
        for file in files:
            with open(file,'rb') as f:
                output.write(f.read())
    print(f'Finished Downloading {filename}')
def _download_file(url,filename,filesize,threads):
    global kill_threads
    kill_threads = False
    temp_dir = tempfile.mkdtemp()
    thread_lists = []
    thread_per_byte = int(filesize / threads)
    progress = tqdm(
        unit='B',
        desc=filename,
        unit_scale=True,
        total=filesize
    )
    for _ in range(threads):
        filename = f'{temp_dir}/{_}.tmp'
        if _ == 0:
            range_header = {'Range':f'bytes=0-{thread_per_byte}'}
            last_byte = thread_per_byte
        else:
            end_byte = last_byte + thread_per_byte
            range_header = {'Range':f'bytes={last_byte}-{end_byte}'}
            last_byte = end_byte
        thread = threading.Thread(target=_download_part,args=(filename,url,range_header,progress))
        thread_lists.append(thread)
        thread.start()
    try:
        if _handle_thread(thread_lists):
            _merge_()
    except KeyboardInterrupt:
        print(f'Killing Threads')
        kill_threads = True

def _download_part(temp_file,url,range_header=None,progress_bar=None,start=None,end=None):
    global kill_threads
    if range_header is None:
        range = {'Range':f'{start}-{end}'}
        range_header = range
    req = requests.get(url,headers=range_header,stream=True)
    with open(temp_file,'wb+')as f:
        for chunk in req.iter_content(1024):
           if kill_threads:
               return
           else:
                f.write(chunk) 
                progress_bar.update(1024)
    