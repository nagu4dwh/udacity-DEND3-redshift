## Project's Overview

This project defines and populates Sparkify's analytical database in an automated manner. It processes log and song data stored in json files on S3 and uploads data into Redshift database.

## Project's structure
* sql_queries.py - a script that stores all SQL queries necessary for creating tables and inserting data in sparkifydb 
* create_tables.py - a script that creates a database and all tables specified in sql_queries.py
* etl.py - an actual script with ETL process, run it to populate the tables in our database 

To better understand the process of transforming raw json data into unified star schema pattern in our database here's an overview of the structure of each table we will create

### Songs data (data/song_data)
Here is the first record of raw song data

| artist_id | artist_latitude | artist_location | artist_longitude | artist_name | duration | num_songs | song_id | title | year
| :------------- | :----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | 
|  ARNNKDK1187B98BBD5 | 45.80726 | Zagreb Croatia | 15.9676 | Jinx | 407.37914 | 1 | SOFNOQK12AB01840FC | Kutt Free (DJ Volume Remix) | 0

After ETL process this data will be divided into two separate dimension tables:

#### Songs (dimension)
Song dimension table will look as follows:

| song_id | title | artist_id | year | duration 
| :------------- | :----------: | -----------: | -----------: | -----------: |
|  SOFNOQK12AB01840FC | Kutt Free (DJ Volume Remix) | ARNNKDK1187B98BBD5 | None | 407.37914


#### Artists (dimension)
Artist dimension table will look as follows:

| artist_id | name | location | latitude | longitude 
| :------------- | :----------: | -----------: | -----------: | -----------: |
|  ARNNKDK1187B98BBD5 | Jinx | Zagreb Croatia | 45.80726 | 15.9676


### Logs data (data/logs_data)
Here is the first record of raw logs data

| artist | auth | firstName | gender | itemInSession | lastName | length | level | location | method | page | registration | sessionId | song | status | ts | userAgent | userId
| :------------- | :----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: |  -----------: |  -----------: |  -----------: |  -----------: |  -----------: |  -----------: |  -----------: |  -----------: |
|  Sydney Youngblood | Logged In | Jacob | M | 53 | Klein | 238.07955 | paid | Tampa-St. Petersburg-Clearwater, FL | PUT | NextSong | 1.540558e+12 | 954 | Ain't No Sunshine | 200 | 2018-11-29 00:00:57.796 | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4... | 73


#### Time (dimension)
Time dimension table will look as follows:

| start_time | hour | day | week | month | year | weekday 
| :------------- | :----------: | -----------: | -----------: | -----------: | -----------: | -----------: |
|  2018-11-29 00:00:57.796 | 0 | 29 | 48 | 11  | 2018 | 3

#### Users (dimension)
Users dimension table will look as follows:

| userId | firstName | lastName | gender | level
| :------------- | :----------: | -----------: | -----------: | -----------: | 
|  73 | Jacob | Klein | M | paid 

#### Songplays (fact)

| songplay_id | start_time | user_id | level | song_id | artist_id | session_id | location | user_agent 
| :------------- | :----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: | -----------: |
|  1 | 2018-11-29 00:00:57.796000 | 73 | paid | None | None | 954 | Tampa-St. Petersburg-Clearwater, FL | Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2

## Execute 

In order to create the database and populate all necessary tables you should do the following steps:
1. Run `etl.py`

## Database schema

Information in sparkifydb is organized according to star schema design pattern. As mentioned above it has one fact table `songplays` and four dimension tabes `time`, `artists`, `songs`, `users`.

Database schema is as follows:

![Sparkify db schema](https://i.imgur.com/ms4l54B.jpg)