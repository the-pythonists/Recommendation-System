'''
Script to fill data in databse using selenium.

Approach used in this programm is to get data from local system(thumbnail and video) and from tmdb using it's API to fill data
Database

Main motive behind this programm is to upload approx 100 videos with proper data.
So, the approach used here is simple & basic.
'''

# Importing neccessary packages
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import requests
import os
import tmdbsimple as tmdb
import json

# creating driver object
# we will use chrome for our purpose here
driver = webdriver.Chrome()

# local host url of our website
url = "http://127.0.0.1:8000/upload/"
driver.get(url)

# get input elements of login page by their ID's
email = driver.find_element_by_id('uname1')
pswd = driver.find_element_by_id('pwd1')

# passing email and password to login
user = 'mohammad.danish2694@gmail.com'
pwd = '1234'

email.send_keys(user)
pswd.send_keys(pwd)

# click the Login button
login = driver.find_element_by_id('btnLogin')
login.click()

# define tmdb API_Key to obtain video details such as movie category and Video Description
tmdb.API_KEY = 'Your_Api_Key_Here'

# Initialize the tmdb search object
search = tmdb.Search()

# making get request to fetch all the movie genre's and their ID's
# because the search.movie returs movie genre's in the form of list containing genre ID's
# we will use those ID's to get genre Names from this url response

# once we get the response, convert it into json to fetch the data
r = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=<<Your_Api_Key_Here>>&language=en-US')
json_data = json.loads(r.text)
genre_id = (json_data['genres'])

# running a loop inside video directory  
# checking for valid video extension (all videos are in .mp4 format only)
for movie in os.listdir('E:\\DB\\Videos\\'):
	movie_category = ''
	if movie.endswith('.mp4'):

		# pass the movie name in search.movie()
		# make sure it is proper movie name without any irrelevant or extra characters
		# for e.g. movie name should be 'Baahubali' and not 'Baahubali - Official Trailer' or something similar.
		# The trailers which I downloaded using video_downloader.py file follows the same pattern as 'Baahubali - Official Trailer'
		# so spliting the file name to get the proper movie name

		response = search.movie(query=movie.split('-')[0])

		# search.movie returns a list of jsons,
		# we will get the first element and target the 'poster_path' key which containes the poster url
		i = search.results[0]

		# getting 'genre_ids' key from the response which is actually an array of integers
		gid = i['genre_ids']

		# fetching genre names from genre ID's which we got from search.movie response
		# appending movie genres in movie_category to get all the possible genres/categories
		for gd in genre_id:
			if gd['id'] in gid:
				movie_category = movie_category + ' '+ gd['name']
		
		print(movie.split('.')[0]+'.jpg')

		# now we will get the 'overview' key to fetch the Movie Description
		overview = i['overview']

		# opening the upload page
		# previously this url redirected to login page
		# once we login, this url will open the video upload page
		driver.get(url)

		# get all the input elements by their ID's
		thumb = driver.find_element_by_id('thumbnail')
		video = driver.find_element_by_id('video')
		title = driver.find_element_by_id('title')
		cat = driver.find_element_by_id('category')
		desc = driver.find_element_by_id('description')

		# now we have all the data to be passed in input fields
		# video name and video poster name is same but with different extensions(obviously)
		# so removing '.mp4' from file name and adding '.jpg' to get the image name
		# We are using video file name as our title but without file extension
		thumb.send_keys('E:\\DB\\Videos\\'+str(movie.split('.')[0])+'.jpg')
		video.send_keys('E:\\DB\\Videos\\'+movie)
		title.send_keys(movie.split('.')[0])
		cat.send_keys(movie_category)
		desc.send_keys(overview)

		save = driver.find_element_by_id('submit')
		save.click()