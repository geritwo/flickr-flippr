
init_db = """
CREATE TABLE IF NOT EXISTS photo_pool (
  img_id SERIAL PRIMARY KEY,
  title VARCHAR NOT NULL,
  description VARCHAR,
  date_taken VARCHAR,
  date_upload INT,
  is_public INT,
  is_friend INT,
  is_family INT,
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
  context_id INT
);
"""

insert_script = """
INSERT INTO photo_pool 
    (title, description, 
    date_taken, date_upload,
    is_public, is_friend, is_family, 
    tags,
    latitude, longitude,
    original_format, o_width, o_height,
    secret, original_secret,
    server, farm, context)
VALUES (%s, %s, 
    %s, %s,
    %s,
    %s, %s,
    %s, %s, %s,
    %s, %s,
    %s, %s, %s);
"""



