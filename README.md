# Animeout

**Animeout** downloads your favorite Anime series
```>>> import animeout
>>> animeout.scrape_direct('https://www.animeout.xyz/haikyuu-karasuno-koukou-vs-shiratorizawa-gakuen-koukou/')
What quality you want? ['1080', '720']: 720
10 Download links
Do you wish to download the files? Y/n: Y
Downloading [AnimeOut] Haikyuu!! Karasuno High School vs. Shiratorizawa Academy - 01 [720p][Commie][AKS].mkv...
[AnimeOut] Haikyuu!! Karasuno High School vs. Shiratorizawa Academy - 01 [720p][Commie][AKS].mkv:   1%|▏                    | 1.74M/219M [00:01<02:01, 1.79MB/s]
```
**Documentation**

```
scrape_direct(url,json=False)
```
Scrapes links from the target series(`https://www.animeout.xyz/haikyuu-karasuno-koukou-vs-shiratorizawa-gakuen-koukou/`) and sorts qualities.
```
scrape_mega(url,json=False)
```
Returns an list object that contains a list of MEGA urls

```
downloads(urls,threads=2,directory=None)
```
Function that supports urls as list and download them one by one and this where `download` comes
```
download(url,threads=None,directory=None)
```

Download the video file if directory is set, it will saved from the location where it was set(`directory`)


**Feel free to PR.**
