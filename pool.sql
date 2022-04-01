CREATE TABLE IF NOT EXISTS PhotoPool (
  img_id SERIAL PRIMARY KEY,        -- AUTO_INCREMENT integer, as primary key
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
  original_format INT,
  o_width INT,
  o_height INT,
  secret INT,
  original_secret INT,
  server INT,
  farm INT,
  context INT
);

ALTER TABLE IF EXISTS public."PhotoPool"
    OWNER to postgres;