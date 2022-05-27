import flickrapi
import webbrowser
import logging

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


def init_flickr(api_key, api_secret) -> object:
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

    print('Step 1: authenticate')

    # Only do this if we don't have a valid token already
    if not flickr.token_valid(perms='read'):
        flickr.get_request_token(oauth_callback='oob')

        authorize_url = flickr.auth_url(perms='read')
        webbrowser.open_new_tab(authorize_url)

        verifier = str(input('Verifier code: '))
        flickr.get_access_token(verifier)

    return flickr


def get_photos_from_flickr(flickr, page) -> object:
    photos = flickr.people.getPhotos(user_id=FLICKR_USER_ID,
                                     page=page,
                                     extras='tags,'
                                            'description,'
                                            'original_format,'
                                            'o_dims,'
                                            'date_taken,'
                                            'date_upload,'
                                            'geo,'
                                            'url_t,'
                                            'url_m,'
                                            'url_o'
                                     )

    return {
        'TotalPages': photos['photos']['pages'],
        'CurrentPage': photos['photos']['page'],
        'PhotosList': photos['photos']['photo']
    }


def create_database(connection) -> None:
    cur = connection.cursor()
    cur.execute("""
        DROP TABLE IF EXISTS photo_pool;
        CREATE TABLE photo_pool (
        img_id            SERIAL PRIMARY KEY,
        title             VARCHAR NOT NULL,
        description       VARCHAR,
        date_taken        VARCHAR,
        date_upload       INT,
        is_public         INT,
        is_friend         INT,
        is_family         INT,
        tags              VARCHAR,
        latitude          FLOAT,
        longitude         FLOAT,
        original_format   VARCHAR,
        o_width           INT,
        o_height          INT,
        secret            VARCHAR,
        original_secret   VARCHAR,
        server            VARCHAR,
        farm              INT,
        context_id        INT,
        url_thumb         VARCHAR,
        url_preview       VARCHAR,
        url_original      VARCHAR
    );
    """)
    connection.commit()


def store_meta_in_db(connection, photos_list) -> None:
    cur = connection.cursor()
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
                        server, farm, context_id,
                        url_thumb, url_preview, url_original)
                    VALUES (
                        %(title)s, %(description)s, 
                        %(datetaken)s, %(dateupload)s,
                        %(ispublic)s, %(isfriend)s, %(isfamily)s, 
                        %(tags)s,
                        %(latitude)s, %(longitude)s,
                        %(originalformat)s, %(o_width)s, %(o_height)s,
                        %(secret)s, %(originalsecret)s,
                        %(server)s, %(farm)s, %(context)s,
                        %(url_t)s, %(url_m)s, %(url_o)s
                    ); 
                """, {
                        **photo,
                        "description": photo['description']['_content'],
                        "url_m": photo['url_m'] if 'url_m' in list(photo.keys()) else ""
                })
        connection.commit()


def store_all_photos(connection, flickr_reader):
    current_page = 1
    while True:
        photos_meta = get_photos_from_flickr(flickr_reader, current_page)
        logging.info(f"Getting photos meta from page {photos_meta['CurrentPage']}...")
        store_meta_in_db(connection, photos_meta['PhotosList'])
        current_page += 1
        if current_page > photos_meta['TotalPages']:
            break


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)

    conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME,
                            user=DB_USER, password=DB_PASSWORD,
                            port=5432)
    logging.info("Established DB connection")

    flickr_reader = init_flickr(API_KEY, API_SECRET)
    logging.info("Intialized access to Flickr")

    create_database(conn)
    logging.info("Recreated Database")
    logging.info("Begin requesting and storing metadata")
    store_all_photos(conn, flickr_reader)

    logging.info("Done.")
