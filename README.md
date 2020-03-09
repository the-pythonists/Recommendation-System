# Recommendation-System
### An aproach towards Content Based Recommendation System

In order to make the Recommendation System, there has to some data in Data Base which can be used to play Recommended videos.

Collecting data and then uploading into database manually was boring and tiredsome.
So I tried to automate this task.

First, I downloaded the movie trailers
```
this is an interactive approach towards recommendation System, so I decided to go with Movie Trailers
```

To download the videos, ***'video_downloader.py'*** file is used.

Then to provide thumbnails to the videos, I downloaded the movie posters using ***'movie_poster_downloader.py'*** file.

And finally, video upload is done using ***'video_uploader.py'*** which is actually web automation technique to automatically upload the Data.

# Sources and Documentation:-

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

https://pypi.org/project/pytube/

https://pypi.org/project/tmdbsimple/

https://www.selenium.dev/selenium/docs/api/py/api.html

https://pypi.org/project/selenium/
