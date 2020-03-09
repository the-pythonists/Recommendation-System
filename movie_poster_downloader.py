'''
Script to download movie posters.

Approach used in this programm is to extract the poster url from The Movie DataBase(tmdb) using API, appending it with base url 
i.e. 'http://image.tmdb.org/t/p/original' and saving the image. To get this script running, tmdb API Key will be required

To register for an API key, click the API Link from within your account settings page.

Click on your avatar or initials in the main navigation
Click the "Settings" link
Click the "API" link in the left sidebar
Click "Create" or "click here" on the API page

Comlplete documentation is available at 'https://developers.themoviedb.org/3/getting-started/introduction'

'''

# Importing necessary packages

import requests
import os
import tmdbsimple as tmdb

# define your API_KEY here
tmdb.API_KEY = 'Your_API_Key_Here'

# Creating tmdb search instance
search = tmdb.Search()

# running a loop inside video directory  
# checking for valid video extension (all videos are in .mp4 format only)
for movie in os.listdir('E:\\DB\\Videos\\'):
	if movie.endswith('.mp4'):

		# pass the movie name in search.movie()
		# make sure it is proper movie name without any irrelevant or extra characters
		# for e.g. movie name should be 'Baahubali' and not 'Baahubali - Official Trailer' or something similar.
		# The trailers which I downloaded using video_downloader.py file follows the same pattern as 'Baahubali - Official Trailer'
		# so spliting the file name to get the proper movie name

		response = search.movie(query=movie.split('-')[0])
		
		# search.movie returns a list of jsons,
		# we will get the first element and target the 'poster_path' key which containes the poster url
		# if 'poster_path' is none in first json, we will get the second json and extract the 'poster_path'
		i = search.results[0]
		j = i['poster_path']
		if j == None:
			i = search.results[1]
			j = i['poster_path']
		print(movie.split('-')[0])

		# finally after getting the poster url, 
		# append it with the base url and download the image
	try:
		img_data = requests.get('http://image.tmdb.org/t/p/original'+j).content
		with open(movie+'.jpg', 'wb') as handler:
		    handler.write(img_data)
	except:
		print('File Not Found')