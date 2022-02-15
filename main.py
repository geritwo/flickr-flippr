import flickrapi
import os

try:
  API_KEY = os.environ['FLICKR_API_KEY'] 
  API_SECRET = os.environ['FLICKR_API_SECRET']
except Error as e:
  raise e

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets.getList(user_id='73509078@N00')

print(sets)

