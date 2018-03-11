'''
Tweetbot for regular posting of revision notes

Created 30 Sept 2013

@author: Kenneth Ban (kennethban@gmail.com)

**Edited to work in the Django Web App
'''

# import modules
# non-std library items: ConfigParser, twython

import os
import logging
import sqlite3
import random
from twython import Twython, TwythonError
from datetime import datetime

# define helper functions

def weighted_choice(d):
    for key in d:
        d[key] = int(d[key])
    r = random.uniform(0,sum(d.values()))
    s = 0.0
    for k,w in d.items():
        s+=w
        if r<s: return k
    return k

def weekday(day):
    days = {'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6}
    return days[day]

def tweetday(today,schedule_days):
    if today in schedule_days:
        return True
    else:
        return False

def get_twitter_handle(apt, aps, act, acs):
    twitter = Twython(apt, aps, act, acs)
    return twitter.verify_credentials()["screen_name"]

## methods to modularize main
def connect_db(db_file):
    try:
        con = sqlite3.connect(db_file)
        return con
    except sqlite3.DatabaseError:
        logging.critical('Cannot load database')
    return None

def get_twitter_profile_config_from_db(cur):
    ct = cur.execute("SELECT consumer_token FROM botapp_twitterprofile WHERE id = 1").fetchone()[0]
    cs = cur.execute("SELECT consumer_secret FROM botapp_twitterprofile WHERE id = 1").fetchone()[0]
    at = cur.execute("SELECT access_token FROM botapp_twitterprofile WHERE id = 1").fetchone()[0]
    ac = cur.execute("SELECT access_secret FROM botapp_twitterprofile WHERE id = 1").fetchone()[0]
    return ct, cs, at, ac

def dictify(rows):
    new_dict = dict()
    for row in rows:
        new_dict[row[1]] = str(row[2])
    return new_dict

def get_topic_configuration(cur):
    rows = cur.execute("SELECT * FROM botapp_topic").fetchall()
    topics = dictify(rows)
    return topics

def get_schedule(cur):
    schedule = []
    days = cur.execute("SELECT * FROM botapp_schedule WHERE id = 1").fetchone()[1:]
    for day in range(7):
        if(days[day]==1):
            schedule.append(day)
    return schedule

def check_todays_schedule(current):
    schedule_days = get_schedule(current)
    today = datetime.now().date().weekday()
    if not tweetday(today,schedule_days):
        logging.info('Not scheduled day')
        return False
    else:
        return True

def get_twitter_authentication(current):
    consumer_token, consumer_secret, access_token, access_secret = get_twitter_profile_config_from_db(current)
    twitter = Twython(consumer_token, consumer_secret, access_token, access_secret)
    try:
        twitter.verify_credentials()
    except TwythonError as e:
        logging.critical('Cannot authenticate with Twitter: %s',e)
        return False
    return twitter

def check_unposted_and_reset(cur, con):
    cur.execute("SELECT topic FROM tweetmodel_note WHERE count = 0")
    records = cur.fetchall()

    # reset counts
    if len(records) == 0:
        cur.execute("UPDATE tweetmodel_note SET count=0")
        con.commit()
        cur.execute("SELECT topic FROM tweetmodel_note WHERE count=0")
        records = cur.fetchall()

    return records

def get_priority_topic(cur, records):
    topic_priority = get_topic_configuration(cur)
    topics = [x[0] for x in records]
    topics_weighted = {k:topic_priority.get(k) if topic_priority.get(k) else '0' for k in topics }
    topic_choice = weighted_choice(topics_weighted)
    return topic_choice

def get_note_to_tweet(cur, topic_choice):
    cur.execute("SELECT id from tweetmodel_note where topic=? AND count=0",(topic_choice,))
    records = cur.fetchall()
    ids = [x[0] for x in records]
    note_choice = random.choice(ids)
    return note_choice

def write_tweet(current, note_choice):
    current.execute("SELECT note,link from tweetmodel_note where id=?",(note_choice,))
    record = current.fetchone()
    note = record[0]
    link = record[1]
    if link:
        tweet = note + " " + link
    else:
        tweet = note
    return tweet

def post_tweet(twitter, tweet):
    try:
        twitter.update_status(status=tweet)
    except TwythonError as e:
        logging.critical('Unable to post tweet: %s',e)
        exit()

def update_db_and_get_remaining_notes_number(current, con, note_choice, topic_choice):
    current.execute("UPDATE tweetmodel_note SET count=count+1 WHERE id=?",(note_choice,))
    current.execute("INSERT into tweetmodel_history(note_id,topic,timestamp) VALUES(?,?,?)",(note_choice,topic_choice,datetime.now()))
    con.commit()
    current.execute("SELECT topic from tweetmodel_note where count=0")
    records = current.fetchall()
    return len(records)

def initializing():
    # set directories, change to current working directory where all config/database/log files reside
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # enable logging
    logging.basicConfig(filename='tweetbot.log',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Started')

    # get database
    logging.info('Loading database')
    con = connect_db('../db.sqlite3')
    current = con.cursor()
    return con, current

def complete(con, current, message):
    # close database
    current.close()
    con.close()
    if message == 'Completed':
        logging.info('Completed')
    return message

# main
def tweet_note(note_choice):
    con, current = initializing()
    message = "Completed"

    twitter = get_twitter_authentication(current)
    if twitter != False:
        topic_choice = current.execute("SELECT topic from tweetmodel_note where id=?",(note_choice,)).fetchone()[0]

        # get note,link for the selected id
        tweet = write_tweet(current, note_choice)
        print(tweet)

        # post tweet
        #HERE STOP HERE
        post_tweet(twitter, tweet)
        logging.info('Posted tweet: %s %s %s', topic_choice, note_choice, tweet)

        # update count of note that was tweeted, and update history
        # log number of remaining unposted notes
        unposted = update_db_and_get_remaining_notes_number(current, con, note_choice, topic_choice)
        logging.info('Note(s) left: %s', unposted)
    else:
        message = 'Twitter authentication error'

    return complete(con, current, message)

def run():
    con, current = initializing()

    # check if today is on schedule for tweeting
    scheduled = check_todays_schedule(current)
    message = "Completed"
    if scheduled:
        # check twitter authentication first and abort if fails
        twitter = get_twitter_authentication(current)
        if twitter != False:
            # check if any unposted notes
            # if none left, reset counts in the database
            records = check_unposted_and_reset(current, con)

            # get topics and select based on priority
            topic_choice = get_priority_topic(current, records)

            # get ids within topic choice and choose randomly
            note_choice = get_note_to_tweet(current, topic_choice)

            # get note,link for the selected id
            tweet = write_tweet(current, note_choice)

            # post tweet
            #HERE STOP HERE
            post_tweet(twitter, tweet)
            logging.info('Posted tweet: %s %s %s', topic_choice, note_choice, tweet)

            # update count of note that was tweeted, and update history
            # log number of remaining unposted notes
            unposted = update_db_and_get_remaining_notes_number(current, con, note_choice, topic_choice)
            logging.info('Note(s) left: %s', unposted)
            message = 'Tweeted out : ' + tweet
        else:
            message = 'Twitter authentication error'
    else:
        message = 'Today is not the scheduled day'

    return complete(con, current, message)
