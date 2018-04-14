
# coding: utf-8

# In[ ]:


import nltk
from nltk.tokenize import TweetTokenizer
import json
import re
import string
from nltk.corpus import stopwords
import csv
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from autocorrect import spell
import itertools
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import argparse


# In[ ]:


def preprocessTweet(tweet):
    tokenizer = TweetTokenizer()
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    stop_words_english = set(stopwords.words('english'))
    stop_words_english.remove("not") 
    
    tweet = tweet.encode('utf-16', 'surrogatepass').decode('utf-16')
    
    #Remove Urls 

    tweet.replace("don't","do not")
    tweet.replace("can't","can not")
    tweet.replace("cant","can not")
    tweet.replace("dont","do not")
    tweet.replace("isn't","is not")
    tweet.replace("won't","will not")
    tweet.replace("shouldn't","should not")
    tweet.replace("wouldn't","would not")
    
    tweet = ''.join(''.join(s)[:2] for _, s in itertools.groupby(tweet))
    tweet = re.sub(r"http\S+", "", tweet) 
    
    tokens = tokenizer.tokenize(tweet)
    
    #Capture retweets
    if tokens[0] == "RT":
        retweet = tokens[1][1:]
        tokens.remove("RT")
        tokens = tokens[1:]
    
    elif tokens[0] != "RT":
        retweet = ""
    
    #Remove the final ellipses in a tweet
    tokens = tokens[:-1]
   
    #Remove words with numbers in them
    tweet = ' '.join(s for s in tokens if not any(c.isdigit() for c in s))
    tweet = re.sub(r'([^a-zA-Z0-9])\1{3,}',"", tweet)

    tokens = tokenizer.tokenize(tweet)
    remove_tokens = []
    
    for token in tokens:
        if token in string.punctuation:
            remove_tokens.append(token)
        if token[0] == "#":
            remove_tokens.append(token)
        if token[0] == "@":
            remove_tokens.append(token)
        if not token.isalpha():
            remove_tokens.append(token)
    
    cleaned_tokens = [token for token in tokens if token not in remove_tokens]
    
    cleaned_tokens = [lemmatizer.lemmatize(token) for token in cleaned_tokens]
    cleaned_tokens = [spell(token) for token in cleaned_tokens]
    cleaned_tokens = [w.lower() for w in cleaned_tokens if not w.lower() in stop_words_english]
    #cleaned_tokens = [stemmer.stem(token) for token in cleaned_tokens]
    
    return ' '.join(cleaned_tokens),retweet

def preprocessLocation(dic):
    geolocator = Nominatim()
    loc_final = []
    coordinates = []
    try: 
        if 'tweet_location_city' in dic:
            loc = geolocator.geocode(dic['tweet_location_city'],addressdetails=True,language='en')
            if loc is None:
                loc_final = []
            else:
                loc_str = str(loc)
                loc_list = loc_str.split(',')
                #print(loc.raw)
                city = loc_list[0]
                loc_final.append(city)
                if not "state" in loc.raw["address"]:
                    state = ""
                else:
                    state = loc.raw["address"]["state"]

                if not "country" in loc.raw["address"]:
                    country = ""
                else:
                    country = loc.raw["address"]["country"]

                loc_final.append(state)
                loc_final.append(country)
                location = city + "," + state + "," +country
                c = geolocator.geocode(location)
                if c != None:
                    coordinates.append(str(c.latitude))
                    coordinates.append(str(c.longitude))


        elif dic['location']!= "":
            loc = geolocator.geocode(dic['location'],addressdetails=True,language='en')
            if loc is None:
                loc_final = []
            else:
                loc_str = str(loc)
                loc_list = loc_str.split(',')
                #print(loc.raw)
                city = loc_list[0]
                loc_final.append(city)
                if not "state" in loc.raw["address"]:
                    state = ""
                else:
                    state = loc.raw["address"]["state"]

                if not "country" in loc.raw["address"]:
                    country = ""
                else:
                    country = loc.raw["address"]["country"]

                loc_final.append(state)
                loc_final.append(country)
                location = city + "," + state + "," +country
                c = geolocator.geocode(location)
                if c != None:
                    coordinates.append(str(c.latitude))
                    coordinates.append(str(c.longitude))
        
        return loc_final,coordinates
        
    except GeocoderTimedOut:
        return preprocessLocation(dic)

def write_data(lines_data,outfile):
    i = 0
    for line in lines_data[809:]:
        #print(line)
        dic = json.loads(line)
        name  = dic["screen_name"]
        text,retweet = preprocessTweet(dic["text"])
        if "hashtags_in_the_tweet" in dic:        
            hashtags = dic["hashtags_in_the_tweet"]
        else:
            hashtags = []

        if "Mentions_in_the_tweet" in dic:     
            mentions = dic["Mentions_in_the_tweet"]
        else:
            mentions = []
        if "retweet_count" in dic:
            retweet_count = dic["retweet_count"]
        else:
            retweet_count = 0

        if "replied_to" in dic:
            replied_to = dic["replied_to"]
            if replied_to != 'null':
                replied_to = dic["replied_to"]
            else:
                replied_to == 'null'
        else:
            replied_to == 'null'

        #loc_final,coordinates = preprocessLocation(dic)
        loc = dic["location"]
        loc_final = loc.split(",")
        #print(loc_final)

        #print(coordinates)    
        #row = name + "," + text + "," + retweet + "," + '-'.join(mentions) + "," + '-'.join(hashtags) + "," + str(retweet_count) + "," + str(replied_to) +","+ '-'.join(loc_final) + "," + ','.join(coordinates) + "\n"
        row = name + "," + text + "," + retweet + "," + '-'.join(mentions) + "," + '-'.join(hashtags) + "," + str(retweet_count) + "," + str(replied_to) +","+ '-'.join(loc_final) + "\n"
        outfile.write(row)

        i += 1
        if i%1000 == 0:
            print(i)

    outfile.close()
    


# In[ ]:


parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputFile", type=string,help="The file containing the Raw Tweets")
parser.add_argument("-o", "--outputFile", type=string,help="The name of the Output file to be generated")

args = parser.parse_args()

data_file = open(args.inputFile, encoding='utf-8')
outfile = open(args.outputFile,'w')
#writer = csv.writer(outfile)
header = "name,tweet,retweet,mentions,hashtags,retweet_count,replied_to,location"
outfile.write(header+ "\n")

lines_data = data_file.readlines() 
print(len(lines_data))
write_data(lines_data,outfile)

