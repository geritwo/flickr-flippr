import flickrapi
import webbrowser

from psql_helper import *
import os
import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'flickrflippr'
DB_USER = 'postgres'

try:
    API_KEY = os.environ['FLICKR_API_KEY']
    API_SECRET = os.environ['FLICKR_API_SECRET']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    FLICKR_USER_ID = os.environ['FLICKR_USER_ID']
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
photos = flickr.people.getPhotos(user_id=FLICKR_USER_ID, extras='tags,'
                                                         'description,'
                                                         'original_format,'
                                                         'o_dims,'
                                                         'date_taken,'
                                                         'date_upload,'
                                                         'geo')

pages_total = photos['photos']['pages']
photos_list = photos['photos']['photo']

print('Step 3: use PSQL')
conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                        user=DB_USER, password=DB_PASSWORD,
                        port=5432)

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, data VARCHAR);")

cur.execute(init_db)
conn.commit()

for photo in photos_list:
    cur.execute("""
                INSERT INTO photo_pool (
                    title, description, 
                    date_taken, date_upload,
                    is_public, is_friend, is_family, 
                    tags,
                    latitude, longitude,
                    original_format, o_width, o_height,
                    secret, original_secret,
                    server, farm, context_id)
                VALUES (
                    %(title)s, %(description)s, 
                    %(date_taken)s, %(date_upload)s,
                    %(is_public)s, %(is_friend)s, %(is_family)s, 
                    %(tags)s,
                    %(latitude)s, %(longitude)s,
                    %(original_format)s, %(o_width)s, %(o_height)s,
                    %(secret)s, %(original_secret)s,
                    %(server)s, %(farm)s, %(context_id)s
                ); 
                """,
                {
                    "title": photo['title'], "description": photo['description']['_content'],
                    "date_taken": photo['datetaken'], "date_upload": int(photo['dateupload']),
                    "is_public": int(photo['ispublic']), "is_friend": int(photo['isfriend']),
                    "is_family": int(photo['isfamily']),
                    "tags": photo['tags'],
                    "latitude": int(photo['latitude']), "longitude": int(photo['longitude']),
                    "original_format": photo['originalformat'],
                    "o_width": int(photo['o_width']), "o_height": int(photo['o_height']),
                    "secret": photo['secret'], "original_secret": photo['originalsecret'],
                    "server": photo['server'], "farm": int(photo['farm']), "context_id": int(photo['context'])
                })
    conn.commit()

cur.close()
conn.close()
