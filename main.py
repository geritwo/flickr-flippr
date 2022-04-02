import flickrapi
import webbrowser

from psql_helper import *
import os
import psycopg2
import pprint

USER_ID = '55142701@N00'

DB_HOST = 'localhost'
DB_NAME = 'flickrflippr'
DB_USER = 'postgres'

try:
    API_KEY = os.environ['FLICKR_API_KEY']
    API_SECRET = os.environ['FLICKR_API_SECRET']
    DB_PASSWORD = os.environ['DB_PASSWORD']
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
photos = flickr.people.getPhotos(user_id=USER_ID, extras='tags,'
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
    meta_data = (
        photo['title'], photo['description']['_content'],
        photo['datetaken'], int(photo['dateupload']),
        int(photo['ispublic']), int(photo['isfriend']), int(photo['isfamily']),
        photo['tags'],
        int(photo['latitude']), int(photo['longitude']),
        photo['originalformat'], int(photo['o_width']), int(photo['o_height']),
        photo['secret'], photo['originalsecret'],
        photo['server'], int(photo['farm']), int(photo['context']),
    )
    print(meta_data)
    #cur.execute(insert_script, meta_data)
    cur.execute("""
                INSERT INTO photo_pool (title, date_taken)
                VALUES (%(title)s, %(date_taken)s);
                 """,
                {'title': photo['title'], 'date_taken': photo['datetaken']})
    conn.commit()

cur.close()
conn.close()
