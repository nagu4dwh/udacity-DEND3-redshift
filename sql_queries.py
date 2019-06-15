import configparser

# CONFIG
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

ARN = config.get('IAM_ROLE','ARN')
SONG_DATA = config.get('S3','SONG_DATA')
LOG_DATA = config.get('S3','LOG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS temp_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS temp_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= ("""CREATE TABLE temp_events (
artist text,
auth text,
firstname text,
gender varchar(1),
iteminsession int,
lastname text,
length double precision,
level varchar(4),
location text,
method text,
page text,
registration double precision,
sessionid int,
song text,
status smallint,
ts bigint,
useragent text,
userId int
)
""")

staging_songs_table_create = (""" CREATE TABLE temp_songs (
artist_id text,
artist_latitude double precision,
artist_location text,
artist_longitude double precision,
artist_name text,
duration double precision,
num_songs int,
song_id text,
title text,
year smallint
)
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
songplay_id int IDENTITY(0,1) PRIMARY KEY SORTKEY, 
start_time timestamp NOT NULL, 
user_id int NOT NULL, 
level varchar(4), 
song_id text, 
artist_id text,
session_id int, 
location text, 
user_agent text)
DISTSTYLE EVEN
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id int PRIMARY KEY SORTKEY NOT NULL, 
first_name text, 
last_name text, 
gender varchar(1), 
level varchar(4)) 
DISTSTYLE ALL
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id text PRIMARY KEY SORTKEY NOT NULL, 
title text, 
artist_id text, 
year bigint, 
duration double precision) 
DISTSTYLE ALL
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id text PRIMARY KEY SORTKEY NOT NULL, 
name text, 
location text, 
latitude double precision, 
longitude double precision)
DISTSTYLE ALL
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time timestamp PRIMARY KEY SORTKEY NOT NULL, 
hour smallint, 
day smallint, 
week smallint, 
month smallint, 
year smallint, 
weekday smallint)
DISTSTYLE ALL
""")

# STAGING TABLES

staging_events_copy = ("""
COPY temp_events from '{}'
iam_role '{}'
json 's3://udacity-dend/log_json_path.json';
""").format(LOG_DATA, ARN)

staging_songs_copy = ("""
COPY temp_songs from '{}'
iam_role '{}'
json 'auto'
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = (""" 
INSERT INTO songplays (start_time, user_id, level, song_id, session_id, artist_id, location, user_agent)
SELECT 
    timestamp 'epoch' + ts/1000 * interval '1 second' as start_time,
    userid as user_id,
    level,
    song_id,
    sessionid as session_id,
    artist_id,
    location,
    useragent as user_agent
FROM temp_events e
INNER JOIN temp_songs s ON e.song = s.title AND e.artist = s.artist_name AND e.length = s.duration
""")

user_table_insert = ("""
INSERT INTO users SELECT DISTINCT(userid), firstname, lastname, gender, level FROM temp_events WHERE userid IS NOT NULL
""")

song_table_insert = ("""
INSERT INTO songs SELECT DISTINCT(song_id), title, artist_id, year, duration FROM temp_songs WHERE song_id IS NOT NULL
""")

artist_table_insert = ("""
INSERT INTO artists SELECT DISTINCT(artist_id), artist_name, artist_location, artist_latitude, artist_longitude FROM temp_songs WHERE artist_id IS NOT NULL
""")

time_table_insert = ("""
INSERT INTO time
    SELECT 
        DISTINCT(timestamp 'epoch' + ts/1000 * interval '1 second'),
        extract(hours from timestamp 'epoch' + ts/1000 * interval '1 second') as hour,
        extract(day from timestamp 'epoch' + ts/1000 * interval '1 second') as day,
        extract(week from timestamp 'epoch' + ts/1000 * interval '1 second') as week,
        extract(month from timestamp 'epoch' + ts/1000 * interval '1 second') as month,
        extract(year from timestamp 'epoch' + ts/1000 * interval '1 second') as year,
        extract(dayofweek from timestamp 'epoch' + ts/1000 * interval '1 second') as weekday
    FROM temp_events
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
