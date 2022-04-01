import flickrapi
import webbrowser
import os

try:
    API_KEY = os.environ['FLICKR_API_KEY']
    API_SECRET = os.environ['FLICKR_API_SECRET']
except KeyError as e:
    exit("Error: FLICKR_API_KEY and/or FLICKR_API_SECRET not set in environment.")

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET, format='parsed-json')

print('Step 1: authenticate')

# Only do this if we don't have a valid token already
if not flickr.token_valid(perms='read'):
    # Get a request token
    flickr.get_request_token(oauth_callback='oob')

    # Open a browser at the authentication URL. Do this however
    # you want, as long as the user visits that URL.
    authorize_url = flickr.auth_url(perms='read')
    webbrowser.open_new_tab(authorize_url)

    # Get the verifier code from the user. Do this however you
    # want, as long as the user gives the application the code.
    verifier = str(input('Verifier code: '))

    # Trade the request token for an access token
    flickr.get_access_token(verifier)

print('Step 2: use Flickr')

# Demo functions
resp = flickr.photos.getInfo(photo_id='7658567128')
photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
sets = flickr.photosets.getList(user_id='73509078@N00')

print(sets)
