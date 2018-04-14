
# coding: utf-8

# In[1]:


import tweepy
import json
import argparse
from datetime import timedelta


# In[ ]:


#These authorization details are specific to each person. An application needs to be registered with 
#Twitter to be able to get the below details

consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXX"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


# In[64]:


# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 


# In[65]:


parser = argparse.ArgumentParser()
parser.add_argument("-h", "--hashtag", type=string,help="The hashtag that will be crawled")
parser.add_argument("-s", "--since", type=string,help="The beginning of the time period that data will be crawled from")
parser.add_argument("-u", "--until", type=string,help="Upto the time period that data will be crawled")
parser.add_argument("-o", "--outputFile", type=string,help="The name of the Output file to be generated")

args = parser.parse_args()

outfile = open(args.outputFile, 'w')
i = 0
for status in tweepy.Cursor(api.search,
                           q=args.hashtag,
                           since=args.since, 
                           until=args.until,
                           count=280,
                           result_type='recent',
                           include_entities=True,
                           monitor_rate_limit=True, 
                           wait_on_rate_limit=True,
                           lang="en").items():

    eastern_time = status.created_at - timedelta(hours=4)
    edt_time = eastern_time.strftime('%Y-%m-%d %H:%M')
    
    i = i+1
    if i%1000 == 0:
        print(i)
    data = {}
    data['name'] = status.user.name
    data['screen_name'] = status.user.screen_name
    data['user_ID'] = status.user.id
    data['location'] = status.user.location
    data['text'] = status.text
    data['created_at'] = edt_time
    data['retweet_count'] = status.retweet_count
    data['replied_to'] = status.in_reply_to_screen_name
    hashtags = []
    mentions_tweet = []
    if status.place != None:        
        data['tweet_location_country'] = status.place.country
        data['tweet_location_city'] = status.place.full_name
    if status.entities != None:
        htags = status.entities.get('hashtags')
        for htag in htags:
            hashtags.append(htag['text'])
        data['hashtags_in_the_tweet'] = hashtags   
        
        mentions = status.entities.get('user_mentions')
        for mention in mentions:
            mentions_tweet.append(mention['screen_name'])
        data['Mentions_in_the_tweet'] = mentions_tweet

    outfile.write(json.dumps(data))
    outfile.write('\n')
 
outfile.close()


# In[62]:


import json
ex = open(args.OutputFile,'r')
x = ex.readlines()
for line in x:
    print(line)
    dic = json.loads(line)
    print(dic["name"])
    break
print(len(x))

