
init_db = """
CREATE TABLE IF NOT EXISTS photopool (
  img_id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  description VARCHAR,
  date_taken TIMESTAMP,
  date_upload INT,
  is_public INT NOT NULL,
  is_friend INT NOT NULL,
  is_family INT NOT NULL,
  tags VARCHAR,
  latitude INT,
  longitude INT,
  original_format VARCHAR,
  o_width INT,
  o_height INT,
  secret VARCHAR,
  original_secret VARCHAR,
  server VARCHAR,
  farm INT,
  context INT
);
"""

insert_script_bak = "INSERT INTO photopool (" \
                "title, " \
                "description, " \
                "date_taken, " \
                "date_upload, " \
                "is_public, " \
                "is_friend, " \
                "is_family, " \
                "tags, " \
                "latitude,  " \
                "longitude, " \
                "original_format, " \
                "o_width, " \
                "o_height, " \
                "secret, " \
                "original_secret, " \
                "server, " \
                "farm, " \
                "context)" \
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

insert_script = """
INSERT INTO photopool (title, description, date_taken, date_upload,
    is_public, is_friend, is_family, 
    tags,
    latitude, longitude,
    original_format, o_width, o_height,
    secret, original_secret,
    server, farm, context)
VALUES (%s, %s, %s, %s,
    %s,
    %s, %s,
    %s, %s, %s,
    %s, %s,
    %s, %s, %s)
"""


def get_insert_values(photo):
    return (
        photo['title'], photo['description']['_content'], photo['datetaken'], int(photo['dateupload']),
        int(photo['ispublic']), int(photo['isfriend']), int(photo['isfamily']),
        photo['tags'],
        int(photo['latitude']), int(photo['longitude']),
        photo['originalformat'], int(photo['o_width']), int(photo['o_height']),
        photo['secret'], photo['originalsecret'],
        photo['server'], int(photo['farm']), int(photo['context'])
    )
