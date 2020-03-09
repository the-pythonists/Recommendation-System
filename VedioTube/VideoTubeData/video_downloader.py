'''
Script to Download movie trailers, the approach used here is scrapping youtube video links from website and using those links to
download videos directly from youtube using pytube. 
However, there could be other approach to download the movie trailers, but this is what came to my mind.
I passed url one-by-one in this programme, though this process could have been automated, but I was not completely into Web-Scrapping
and just wanted a simple and reliable approach to dowload all the Trailers available on that site.
'''

# Importing necessary packages

# More detail about pytube is available at 'https://pypi.org/project/pytube/'

from bs4 import BeautifulSoup
import requests
from pytube import YouTube

# url to get movie trailers' links
url = 'https://www.radiocity.in/film/video-channels/Movie-Trailers/3/15/4/4'

# making get request
r = requests.get(url)

# creating BeautifulSoup object
soup = BeautifulSoup(r.content,'html5lib')

# getting 'div' tag with class name containing trailer links
# then 'href' link from 'a' tag
for video in soup.findAll("div",class_='video_list_new'):
	for video_link in video.findAll('a'):
		video_url = video_link.get('href')
		
		# making get request on extracted url to extract Youtube video link
		r1 = requests.get(video_url)

		soup1 = BeautifulSoup(r1.content,'html5lib')

		# craeting BeautifulSoup object, 
		# then getting 'div' tag containig video
		# we need video src to download the video
		# video src is inside the 'iframe' tag
		# video src is the Youtube watch link which is required to download the video
		for link in soup1.findAll("div",class_='main_video'):
			video_src = link.findAll("iframe")[0]['src']
			print(video_src)
			try:
				YouTube('./Videos/'+video_src).streams[0].download()
			except:
				print('Passed')