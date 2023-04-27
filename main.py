# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 00:03:33 2020

@author: Kerem's Laptop
"""


from gooey import Gooey, GooeyParser # for the GUI
from selenium import webdriver #for web scraping
import spacy #for NLP
import praw #for Reddit threads
import pandas as pd #for data science
from psaw import PushshiftAPI #for Reddit comments
import twint #for tweets
import nest_asyncio #for loops
import re #for cleaning text
import dash #for dashboard
from deeppavlov import configs, build_model
import dash_table #for dashboard
import dash_html_components as html #for dashboard
import os
from textblob import TextBlob # for sentiment analysis
import pypatent
import feedparser
import plotly.graph_objs as go
from nltk.chunk import conlltags2tree
from nltk import pos_tag
from nltk.tree import Tree
import dash_core_components as dcc

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],)

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#007ACE"}

def ultimategrabber(text,number,method):
    #if method == "Social_Media_Deep_Pavlov" or method == "Magazines_Deep_Pavlov":
        #ner_model = build_model(configs.ner.ner_ontonotes, download=False) 
    def deeppavlov_magazine_scraper(text,number):
        #Part 1 for Spectrum IEEE
        driver = webdriver.Chrome('./chromedriver') #setting headless chrome browser
        spectrum_dict = []
        driver.get(f"https://spectrum.ieee.org/searchContent?q={text}") #get search results
        driver.implicitly_wait(10) #implicit wait for page to load all results
        search = driver.find_elements_by_class_name("article-title") #html code for the title
        for words in search:
            spectrum_dict.append(words.text)
        spectrum = pd.Series(spectrum_dict)
        spectlabel = ['IEEE'] * len(spectrum)
        spectforlabel = pd.Series(spectlabel)
        finalspectlabel = pd.concat([spectrum,spectforlabel], axis = 1)
        finalspectlabel = finalspectlabel.head(number)
        
        #Part 2 for Popular Science
        driver2 = webdriver.Chrome('./chromedriver')
        popular_dict = []
        driver2.get(f"https://www.popsci.com/search-results/{text}/")
        driver2.implicitly_wait(10)
        search2 = driver2.find_elements_by_class_name("siq-partner-result")
        for words2 in search2:
            popular_dict.append(words2.text)
        popular = pd.Series(popular_dict)
        poplabel = ['PopScience'] * len(popular)
        popforlabel = pd.Series(poplabel)
        finalpoplabel = pd.concat([popular,popforlabel], axis = 1)
        finalpoplabel = finalpoplabel.head(number)
        
        #Part 3 for Wired
        driver3 = webdriver.Chrome(executable_path='chromedriver.exe')
        wired_dict = []
        driver3.get("https://www.wired.com/search/?q="+ text + "&page=1&sort=score")
        search3 = driver3.find_elements_by_class_name("archive-item-component__title")
        for words3 in search3:
            wired_dict.append(words3.text)
        wired = pd.Series(wired_dict)
        wiredlabel = ['Wired'] * len(wired)
        wiredforlabel = pd.Series(wiredlabel)
        finalwiredlabel = pd.concat([wired,wiredforlabel], axis = 1)
        finalwiredlabel = finalwiredlabel.head(number)
        
        #Part 4 for Scientific American
        driver4 = webdriver.Chrome(executable_path='chromedriver.exe')
        sciamerican_dict = []
        driver4.get("https://www.scientificamerican.com/search/?q=" + text)
        search4 = driver4.find_elements_by_class_name("listing__title")
        for words4 in search4:
            sciamerican_dict.append(words4.text)
        sciamerican = pd.Series(sciamerican_dict)
        sciamericanlabel = ['Scientific American'] * len(sciamerican)
        sciamericanforlabel = pd.Series(sciamericanlabel)
        finalsciamericanlabel = pd.concat([sciamerican,sciamericanforlabel], axis = 1)
        finalsciamericanlabel = finalsciamericanlabel.head(number)
        
        #Part 5 for Science Mag
        driver5 = webdriver.Chrome(executable_path='chromedriver.exe')
        scimag_dict = []
        driver5.get("https://search.sciencemag.org/?searchTerm=" + text + "&order=tfidf&limit=textFields&pageSize=10&&")
        driver5.implicitly_wait(10)
        search5 = driver5.find_elements_by_class_name("media__headline")
        for words5 in search5:
            scimag_dict.append(words5.text)
        scimag = pd.Series(scimag_dict)
        scimaglabel = ['Science Mag'] * len(scimag)
        scimagforlabel = pd.Series(scimaglabel)
        finalscimaglabel = pd.concat([scimag,scimagforlabel], axis = 1)
        finalscimaglabel = finalscimaglabel.head(number)
        
        #Part 6 for MIT
        driver6 = webdriver.Chrome(executable_path='chromedriver.exe')
        mit_dict = []
        driver6.get("https://www.technologyreview.com/search/?s=" + text)
        driver6.implicitly_wait(10)
        search6 = driver6.find_elements_by_class_name("teaserItem__title--32O7a")
        for words6 in search6:
            mit_dict.append(words6.text)
        mit = pd.Series(mit_dict)
        mitlabel = ['MIT Tech Review'] * len(mit)
        mitforlabel = pd.Series(mitlabel)
        finalmitlabel = pd.concat([mit,mitforlabel], axis = 1)
        finalmitlabel = finalmitlabel.head(number)
        
        #Part 7 for American Scientist
        driver7 = webdriver.Chrome(executable_path='chromedriver.exe')
        america_dict = []
        driver7.get("https://www.americanscientist.org/search/node/" + text)
        driver7.implicitly_wait(10)
        search7 = driver7.find_elements_by_class_name("title")
        for words7 in search7:
            america_dict.append(words7.text)
        america = pd.Series(america_dict)
        americalabel = ['American Scientist'] * len(america)
        americaforlabel = pd.Series(americalabel)
        finalamericalabel = pd.concat([america,americaforlabel], axis = 1)
        finalamericalabel = finalamericalabel.head(number)
        
        #Part 8 for New Scientist
        driver8 = webdriver.Chrome(executable_path='chromedriver.exe')
        newish_dict = []
        driver8.get("https://www.newscientist.com/search/?q=" + text)
        search8 = driver8.find_elements_by_class_name("card__heading")
        for words8 in search8:
            newish_dict.append(words8.text)
        newish = pd.Series(newish_dict)
        newishlabel = ['New Scientist'] * len(newish)
        newishforlabel = pd.Series(newishlabel)
        finalnewishlabel = pd.concat([newish,newishforlabel], axis = 1)
        finalnewishlabel = finalnewishlabel.head(number)
        
        #Part 9 for ScienceNews
        driver9 = webdriver.Chrome(executable_path='chromedriver.exe')
        scinew_dict = []
        driver9.get("https://www.sciencenews.org/?s=" + text)
        search9 = driver9.find_elements_by_class_name("post-item-river__title___J3spU")
        for words9 in search9:
            scinew_dict.append(words9.text)
        scinew = pd.Series(scinew_dict)
        scinewlabel = ['ScienceNews'] * len(scinew)
        scinewforlabel = pd.Series(scinewlabel)
        finalscinewlabel = pd.concat([scinew,scinewforlabel], axis = 1)
        finalscinewlabel = finalscinewlabel.head(number)
        
        #Combine Part 1, Part 2, and Part 3
        frames = [finalspectlabel, finalpoplabel,finalwiredlabel,finalsciamericanlabel,finalscimaglabel,finalmitlabel,finalamericalabel, finalnewishlabel,finalscinewlabel]
        result = pd.concat(frames) #combine everything
        result.columns = ["Text","Type"]
        
        #Named Entity Recognition tool to acquire only certain objects
        ner_model = build_model(configs.ner.ner_ontonotes, download=False)
        def ner(x):
            good_terms = []
            tokens = ner_model([x])[0][0]
            tags = ner_model([x])[1][0]
            pos_tags = [pos for token, pos in pos_tag(tokens)]
            conlltags = [(token, pos, tg) for token, pos, tg in zip(tokens, pos_tags, tags)]
            ne_tree = conlltags2tree(conlltags)
            original_text = []
            for subtree in ne_tree:
                # skipping 'O' tags
                if type(subtree) == Tree:
                    original_label = subtree.label()
                    original_string = " ".join([token for token, pos in subtree.leaves()])
                    original_text.append((original_string, original_label))
            main_dict = dict(original_text)
            for key in main_dict:
                if main_dict[key] == "PRODUCT":
                    good_terms.append(key)
                if main_dict[key] == "ORG":
                    good_terms.append(key)
                if main_dict[key] == "GPE":
                    good_terms.append(key)
                if main_dict[key] == "LOC":
                    good_terms.append(key)
                if "ORG" not in main_dict.values() and "PRODUCT" not in main_dict.values():
                    good_terms.clear()
            return good_terms
    
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    def deeppavlovscraper(text,number):
        
        nest_asyncio.apply()
        #Part 1: for Reddit threads
        reddit = praw.Reddit(client_id='x6e1LTj2OQnGYw', 
                         client_secret='cKPjQfnskfy1w5IlwLi6Aos-DMU', 
                         user_agent='trialnew', 
                         username='opposity', 
                         password='Samborules123?') 
        all = reddit.subreddit("technology+tech+futurology+engineering+army+navy+airforce+geek+military+scifi+science")
        topics_dict = { "URL":[],"Text":[], "Date":[],"Score":[],"Upvote_Ratio":[]}
        for submission in all.search(text, limit = number):
            topics_dict["URL"].append(submission.url)
            topics_dict["Text"].append(submission.title)
            topics_dict["Date"].append(submission.created_utc)
            topics_dict["Score"].append(submission.score)
            topics_dict["Upvote_Ratio"].append(submission.upvote_ratio)
        topics_data = pd.DataFrame(topics_dict)
        topics_data['Date'] = (pd.to_datetime(topics_data['Date'], unit='s'))
        listeforlabel = ['Reddit Thread'] * number
        dflisteforlabel = pd.Series(listeforlabel)
        upnewdf = pd.concat([topics_data, dflisteforlabel], axis=1)
    
        #Part 2: for Reddit comments
        subbies = ["technology","tech","futurology","engineering","army","navy","airforce","geek","military","scifi","science"]
        api = PushshiftAPI()
        gen = api.search_comments(q = text, subreddit = subbies)
        cache = []
        for c in gen:
            cache.append(c)
            if len(cache) >= number:
                break
        comments_df = pd.DataFrame([thing.d_ for thing in cache])
        commentdf = comments_df[["body","created","score","subreddit"]]
        commentdf.columns=["Text","Date","Score","URL"]
        commentdf['URL'] = 'https://www.reddit.com/r/' + commentdf['URL'].astype(str)
        commentdf['Date'] = (pd.to_datetime(commentdf['Date'], unit='s', errors = "coerce"))
        listforlabel = ['Reddit Comment'] * number
        dflistforlabel = pd.Series(listforlabel)
        newdf = pd.concat([commentdf, dflistforlabel], axis=1)
        
        #Part 3: for Tweets
        c = twint.Config()
        c.Search = text
        c.Limit = number
        c.Pandas = True
        #c.Since 
        #c.Until
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df.head(number)
        necessary_text = Tweets_df.tweet
        necessary_date = Tweets_df.date
        necessary_likes = Tweets_df.nlikes
        necessary_retweets = Tweets_df.nretweets
        necessarylinks= Tweets_df.link
        tweetlabel = ['Tweet'] * len(necessary_text)
        tweforlabel = pd.Series(tweetlabel)
        lastlabel = pd.concat([necessary_text, necessary_date], axis=1)
        finallabel = pd.concat([lastlabel,tweforlabel], axis = 1)
        otherlabel = pd.concat([necessarylinks, finallabel], axis = 1)
        otherlabel.rename(columns = {"link":"URL","tweet":"Text","date":"Date"}, inplace = True)
        final2label = pd.concat([otherlabel, necessary_likes], axis=1)
        final3label = pd.concat([final2label, necessary_retweets], axis=1)
        
        #Combine Part 1, Part 2, Part 3
        result1 = upnewdf.append(newdf, sort=False)
        result = result1.append(final3label,sort=False)
        result.columns = ["URL","Text","Date","Score", "Upvote Ratio", "Type","Likes","Retweets"]
        # Specify symbols to keep in text
        symbols_to_keep = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM:;!-,?.@ \n\"\'"
    
        # Function for removing unknown characters
        remove_unknown_chars = lambda x: ''.join(char for char in x if char in symbols_to_keep)
        # Function for removing all Twitter user tags (@ongunuzaymacar, etc.)
        remove_user_tags = lambda x: re.sub(r'@\w+', '', x)
        # Function for removing all Twitter hashtags (#freetheworld, ect.)
        remove_hash_tags = lambda x: re.sub(r'#\w+', '', x)
        # Function for removing all URLs (www.google.com, etc.)
        remove_urls = lambda x: re.sub(r'(https://|www.)[A-Za-z0-9_.]+', '', x)
        
        def clean_tweets(twoot): #cleaning text
            # Convert to lowercase and remove spaces from beginning
            twoot = str(twoot).lstrip()
            # Remove Twitter-related data
            twoot = remove_user_tags(twoot)
            twoot = remove_urls(twoot)
            twoot = remove_hash_tags(twoot)
            # Remove unwanted characters
            twoot = remove_unknown_chars(twoot)
            # Remove spaces from end and condense multiple spaces into one
            twoot = twoot.rstrip()
            twoot = re.sub(' +', ' ', twoot)
            return twoot
        result["Text"] = result["Text"].apply(clean_tweets)
        f = lambda x: " ".join(x["Text"].split())
        result["Text"] = result.apply(f, axis=1)
        
        ner_model = build_model(configs.ner.ner_ontonotes, download=False)
        def ner(x):
            good_terms = []
            tokens = ner_model([x])[0][0]
            tags = ner_model([x])[1][0]
            pos_tags = [pos for token, pos in pos_tag(tokens)]
            conlltags = [(token, pos, tg) for token, pos, tg in zip(tokens, pos_tags, tags)]
            ne_tree = conlltags2tree(conlltags)
            original_text = []
            for subtree in ne_tree:
                # skipping 'O' tags
                if type(subtree) == Tree:
                    original_label = subtree.label()
                    original_string = " ".join([token for token, pos in subtree.leaves()])
                    original_text.append((original_string, original_label))
            main_dict = dict(original_text)
            for key in main_dict:
                if main_dict[key] == "PRODUCT":
                    good_terms.append(key)
                if main_dict[key] == "ORG":
                    good_terms.append(key)
                if main_dict[key] == "GPE":
                    good_terms.append(key)
                if main_dict[key] == "LOC":
                    good_terms.append(key)
                if "ORG" not in main_dict.values() and "PRODUCT" not in main_dict.values():
                    good_terms.clear()
            return good_terms
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    def spacy_sm_magazine_scraper(text,number):
        #Part 1 for Spectrum IEEE
        driver = webdriver.Chrome('./chromedriver') #setting headless chrome browser
        spectrum_dict = []
        driver.get(f"https://spectrum.ieee.org/searchContent?q={text}") #get search results
        driver.implicitly_wait(10) #implicit wait for page to load all results
        search = driver.find_elements_by_class_name("article-title") #html code for the title
        for words in search:
            spectrum_dict.append(words.text)
        spectrum = pd.Series(spectrum_dict)
        spectlabel = ['IEEE'] * len(spectrum)
        spectforlabel = pd.Series(spectlabel)
        finalspectlabel = pd.concat([spectrum,spectforlabel], axis = 1)
        finalspectlabel = finalspectlabel.head(number)
        
        #Part 2 for Popular Science
        driver2 = webdriver.Chrome('./chromedriver')
        popular_dict = []
        driver2.get(f"https://www.popsci.com/search-results/{text}/")
        driver2.implicitly_wait(10)
        search2 = driver2.find_elements_by_class_name("siq-partner-result")
        for words2 in search2:
            popular_dict.append(words2.text)
        popular = pd.Series(popular_dict)
        poplabel = ['PopScience'] * len(popular)
        popforlabel = pd.Series(poplabel)
        finalpoplabel = pd.concat([popular,popforlabel], axis = 1)
        finalpoplabel = finalpoplabel.head(number)
        
        #Part 3 for Wired
        driver3 = webdriver.Chrome(executable_path='chromedriver.exe')
        wired_dict = []
        driver3.get("https://www.wired.com/search/?q="+ text + "&page=1&sort=score")
        search3 = driver3.find_elements_by_class_name("archive-item-component__title")
        for words3 in search3:
            wired_dict.append(words3.text)
        wired = pd.Series(wired_dict)
        wiredlabel = ['Wired'] * len(wired)
        wiredforlabel = pd.Series(wiredlabel)
        finalwiredlabel = pd.concat([wired,wiredforlabel], axis = 1)
        finalwiredlabel = finalwiredlabel.head(number)
        
        #Part 4 for Scientific American
        driver4 = webdriver.Chrome(executable_path='chromedriver.exe')
        sciamerican_dict = []
        driver4.get("https://www.scientificamerican.com/search/?q=" + text)
        search4 = driver4.find_elements_by_class_name("listing__title")
        for words4 in search4:
            sciamerican_dict.append(words4.text)
        sciamerican = pd.Series(sciamerican_dict)
        sciamericanlabel = ['Scientific American'] * len(sciamerican)
        sciamericanforlabel = pd.Series(sciamericanlabel)
        finalsciamericanlabel = pd.concat([sciamerican,sciamericanforlabel], axis = 1)
        finalsciamericanlabel = finalsciamericanlabel.head(number)
        
        #Part 5 for Science Mag
        driver5 = webdriver.Chrome(executable_path='chromedriver.exe')
        scimag_dict = []
        driver5.get("https://search.sciencemag.org/?searchTerm=" + text + "&order=tfidf&limit=textFields&pageSize=10&&")
        driver5.implicitly_wait(10)
        search5 = driver5.find_elements_by_class_name("media__headline")
        for words5 in search5:
            scimag_dict.append(words5.text)
        scimag = pd.Series(scimag_dict)
        scimaglabel = ['Science Mag'] * len(scimag)
        scimagforlabel = pd.Series(scimaglabel)
        finalscimaglabel = pd.concat([scimag,scimagforlabel], axis = 1)
        finalscimaglabel = finalscimaglabel.head(number)
        
        #Part 6 for MIT
        driver6 = webdriver.Chrome(executable_path='chromedriver.exe')
        mit_dict = []
        driver6.get("https://www.technologyreview.com/search/?s=" + text)
        driver6.implicitly_wait(10)
        search6 = driver6.find_elements_by_class_name("teaserItem__title--32O7a")
        for words6 in search6:
            mit_dict.append(words6.text)
        mit = pd.Series(mit_dict)
        mitlabel = ['MIT Tech Review'] * len(mit)
        mitforlabel = pd.Series(mitlabel)
        finalmitlabel = pd.concat([mit,mitforlabel], axis = 1)
        finalmitlabel = finalmitlabel.head(number)
        
        #Part 7 for American Scientist
        driver7 = webdriver.Chrome(executable_path='chromedriver.exe')
        america_dict = []
        driver7.get("https://www.americanscientist.org/search/node/" + text)
        driver7.implicitly_wait(10)
        search7 = driver7.find_elements_by_class_name("title")
        for words7 in search7:
            america_dict.append(words7.text)
        america = pd.Series(america_dict)
        americalabel = ['American Scientist'] * len(america)
        americaforlabel = pd.Series(americalabel)
        finalamericalabel = pd.concat([america,americaforlabel], axis = 1)
        finalamericalabel = finalamericalabel.head(number)
        
        #Part 8 for New Scientist
        driver8 = webdriver.Chrome(executable_path='chromedriver.exe')
        newish_dict = []
        driver8.get("https://www.newscientist.com/search/?q=" + text)
        search8 = driver8.find_elements_by_class_name("card__heading")
        for words8 in search8:
            newish_dict.append(words8.text)
        newish = pd.Series(newish_dict)
        newishlabel = ['New Scientist'] * len(newish)
        newishforlabel = pd.Series(newishlabel)
        finalnewishlabel = pd.concat([newish,newishforlabel], axis = 1)
        finalnewishlabel = finalnewishlabel.head(number)
        
        #Part 9 for ScienceNews
        driver9 = webdriver.Chrome(executable_path='chromedriver.exe')
        scinew_dict = []
        driver9.get("https://www.sciencenews.org/?s=" + text)
        search9 = driver9.find_elements_by_class_name("post-item-river__title___J3spU")
        for words9 in search9:
            scinew_dict.append(words9.text)
        scinew = pd.Series(scinew_dict)
        scinewlabel = ['ScienceNews'] * len(scinew)
        scinewforlabel = pd.Series(scinewlabel)
        finalscinewlabel = pd.concat([scinew,scinewforlabel], axis = 1)
        finalscinewlabel = finalscinewlabel.head(number)
        
        #Combine Part 1, Part 2, and Part 3
        frames = [finalspectlabel, finalpoplabel,finalwiredlabel,finalsciamericanlabel,finalscimaglabel,finalmitlabel,finalamericalabel, finalnewishlabel,finalscinewlabel]
        result = pd.concat(frames) #combine everything
        result.columns = ["Text","Type"]
        
        #Named Entity Recognition tool to acquire only certain objects
        def ner(x):
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(x)
            textually = []
            tags = []
            for ent in doc.ents:
                textually.append(ent.text)
                tags.append(ent.label_)
            spacy_dictionary = dict(zip(textually,tags))
            good_terms = []
            for key in spacy_dictionary:
                if spacy_dictionary[key] == "ORG":
                    good_terms.append(key)
                if spacy_dictionary[key] == "GPE":
                    good_terms.append(key)
                if spacy_dictionary[key] == "LOC":
                    good_terms.append(key)
                if spacy_dictionary[key] == "PRODUCT":
                    good_terms.append(key)
                if spacy_dictionary[key] == "DATE":
                    good_terms.append(key)
                if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                    good_terms.clear()
            return good_terms
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    def spacy_md_magazine_scraper(text,number):
        
        #Part 1 for Spectrum IEEE
        driver = webdriver.Chrome('./chromedriver')
        spectrum_dict = []
        driver.get(f"https://spectrum.ieee.org/searchContent?q={text}")
        driver.implicitly_wait(10)
        search = driver.find_elements_by_class_name("article-title")
        for words in search:
            spectrum_dict.append(words.text)
        spectrum = pd.Series(spectrum_dict)
        spectlabel = ['IEEE'] * len(spectrum)
        spectforlabel = pd.Series(spectlabel)
        finalspectlabel = pd.concat([spectrum,spectforlabel], axis = 1)
        finalspectlabel = finalspectlabel.head(number)
        
        #Part 2 for Popular Science
        driver2 = webdriver.Chrome('./chromedriver')
        popular_dict = []
        driver2.get(f"https://www.popsci.com/search-results/{text}/")
        driver2.implicitly_wait(10)
        search2 = driver2.find_elements_by_class_name("siq-partner-result")
        for words2 in search2:
            popular_dict.append(words2.text)
        popular = pd.Series(popular_dict)
        poplabel = ['PopScience'] * len(popular)
        popforlabel = pd.Series(poplabel)
        finalpoplabel = pd.concat([popular,popforlabel], axis = 1)
        finalpoplabel = finalpoplabel.head(number)
        
        #Part 3 for Wired
        driver3 = webdriver.Chrome(executable_path='chromedriver.exe')
        wired_dict = []
        driver3.get("https://www.wired.com/search/?q="+ text + "&page=1&sort=score")
        search3 = driver3.find_elements_by_class_name("archive-item-component__title")
        for words3 in search3:
            wired_dict.append(words3.text)
        wired = pd.Series(wired_dict)
        wiredlabel = ['Wired'] * len(wired)
        wiredforlabel = pd.Series(wiredlabel)
        finalwiredlabel = pd.concat([wired,wiredforlabel], axis = 1)
        finalwiredlabel = finalwiredlabel.head(number)
        
        #Part 4 for Scientific American
        driver4 = webdriver.Chrome(executable_path='chromedriver.exe')
        sciamerican_dict = []
        driver4.get("https://www.scientificamerican.com/search/?q=" + text)
        search4 = driver4.find_elements_by_class_name("listing__title")
        for words4 in search4:
            sciamerican_dict.append(words4.text)
        sciamerican = pd.Series(sciamerican_dict)
        sciamericanlabel = ['Scientific American'] * len(sciamerican)
        sciamericanforlabel = pd.Series(sciamericanlabel)
        finalsciamericanlabel = pd.concat([sciamerican,sciamericanforlabel], axis = 1)
        finalsciamericanlabel = finalsciamericanlabel.head(number)
        
        #Part 5 for Science Mag
        driver5 = webdriver.Chrome(executable_path='chromedriver.exe')
        scimag_dict = []
        driver5.get("https://search.sciencemag.org/?searchTerm=" + text + "&order=tfidf&limit=textFields&pageSize=10&&")
        driver5.implicitly_wait(10)
        search5 = driver5.find_elements_by_class_name("media__headline")
        for words5 in search5:
            scimag_dict.append(words5.text)
        scimag = pd.Series(scimag_dict)
        scimaglabel = ['Science Mag'] * len(scimag)
        scimagforlabel = pd.Series(scimaglabel)
        finalscimaglabel = pd.concat([scimag,scimagforlabel], axis = 1)
        finalscimaglabel = finalscimaglabel.head(number)
        
        #Part 6 for MIT
        driver6 = webdriver.Chrome(executable_path='chromedriver.exe')
        mit_dict = []
        driver6.get("https://www.technologyreview.com/search/?s=" + text)
        driver6.implicitly_wait(10)
        search6 = driver6.find_elements_by_class_name("teaserItem__title--32O7a")
        for words6 in search6:
            mit_dict.append(words6.text)
        mit = pd.Series(mit_dict)
        mitlabel = ['MIT Tech Review'] * len(mit)
        mitforlabel = pd.Series(mitlabel)
        finalmitlabel = pd.concat([mit,mitforlabel], axis = 1)
        finalmitlabel = finalmitlabel.head(number)
        
        #Part 7 for American Scientist
        driver7 = webdriver.Chrome(executable_path='chromedriver.exe')
        america_dict = []
        driver7.get("https://www.americanscientist.org/search/node/" + text)
        driver7.implicitly_wait(10)
        search7 = driver7.find_elements_by_class_name("title")
        for words7 in search7:
            america_dict.append(words7.text)
        america = pd.Series(america_dict)
        americalabel = ['American Scientist'] * len(america)
        americaforlabel = pd.Series(americalabel)
        finalamericalabel = pd.concat([america,americaforlabel], axis = 1)
        finalamericalabel = finalamericalabel.head(number)
        
        #Part 8 for New Scientist
        driver8 = webdriver.Chrome(executable_path='chromedriver.exe')
        newish_dict = []
        driver8.get("https://www.newscientist.com/search/?q=" + text)
        search8 = driver8.find_elements_by_class_name("card__heading")
        for words8 in search8:
            newish_dict.append(words8.text)
        newish = pd.Series(newish_dict)
        newishlabel = ['New Scientist'] * len(newish)
        newishforlabel = pd.Series(newishlabel)
        finalnewishlabel = pd.concat([newish,newishforlabel], axis = 1)
        finalnewishlabel = finalnewishlabel.head(number)
        
        #Part 9 for ScienceNews
        driver9 = webdriver.Chrome(executable_path='chromedriver.exe')
        scinew_dict = []
        driver9.get("https://www.sciencenews.org/?s=" + text)
        search9 = driver9.find_elements_by_class_name("post-item-river__title___J3spU")
        for words9 in search9:
            scinew_dict.append(words9.text)
        scinew = pd.Series(scinew_dict)
        scinewlabel = ['ScienceNews'] * len(scinew)
        scinewforlabel = pd.Series(scinewlabel)
        finalscinewlabel = pd.concat([scinew,scinewforlabel], axis = 1)
        finalscinewlabel = finalscinewlabel.head(number)
        
        #Combine Part 1, Part 2, and Part 3
        frames = [finalspectlabel, finalpoplabel,finalwiredlabel,finalsciamericanlabel,finalscimaglabel,finalmitlabel,finalamericalabel, finalnewishlabel,finalscinewlabel]
        result = pd.concat(frames)
        result.columns = ["Text","Type"]
        
        #NER tool
        def ner(x):
            nlp = spacy.load("en_core_web_md")
            doc = nlp(x)
            textually = []
            tags = []
            for ent in doc.ents:
                textually.append(ent.text)
                tags.append(ent.label_)
            spacy_dictionary = dict(zip(textually,tags))
            good_terms = []
            for key in spacy_dictionary:
                if spacy_dictionary[key] == "ORG":
                    good_terms.append(key)
                if spacy_dictionary[key] == "GPE":
                    good_terms.append(key)
                if spacy_dictionary[key] == "LOC":
                    good_terms.append(key)
                if spacy_dictionary[key] == "PRODUCT":
                    good_terms.append(key)
                if spacy_dictionary[key] == "DATE":
                    good_terms.append(key)
                if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                    good_terms.clear()
            return good_terms
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    def spacymdscraper(text,number):
        
        nest_asyncio.apply()
        #Part 1: for Reddit threads
        reddit = praw.Reddit(client_id='x6e1LTj2OQnGYw', 
                         client_secret='cKPjQfnskfy1w5IlwLi6Aos-DMU', 
                         user_agent='trialnew', 
                         username='opposity', 
                         password='Samborules123?') 
        all = reddit.subreddit("technology+tech+futurology+engineering+army+navy+airforce+geek+military+scifi+science")
        topics_dict = { "URL":[],"Text":[], "Date":[],"Score":[],"Upvote_Ratio":[]}
        for submission in all.search(text, limit = number):
            topics_dict["URL"].append(submission.url)
            topics_dict["Text"].append(submission.title)
            topics_dict["Date"].append(submission.created_utc)
            topics_dict["Score"].append(submission.score)
            topics_dict["Upvote_Ratio"].append(submission.upvote_ratio)
        topics_data = pd.DataFrame(topics_dict)
        topics_data['Date'] = (pd.to_datetime(topics_data['Date'], unit='s'))
        listeforlabel = ['Reddit Thread'] * number
        dflisteforlabel = pd.Series(listeforlabel)
        upnewdf = pd.concat([topics_data, dflisteforlabel], axis=1)
    
        #Part 2: for Reddit comments
        subbies = ["technology","tech","futurology","engineering","army","navy","airforce","geek","military","scifi","science"]
        api = PushshiftAPI()
        gen = api.search_comments(q = text, subreddit = subbies)
        cache = []
        for c in gen:
            cache.append(c)
            if len(cache) >= number:
                break
        comments_df = pd.DataFrame([thing.d_ for thing in cache])
        commentdf = comments_df[["body","created","score","subreddit"]]
        commentdf.columns=["Text","Date","Score","URL"]
        commentdf['URL'] = 'https://www.reddit.com/r/' + commentdf['URL'].astype(str)
        commentdf['Date'] = (pd.to_datetime(commentdf['Date'], unit='s', errors = "coerce"))
        listforlabel = ['Reddit Comment'] * number
        dflistforlabel = pd.Series(listforlabel)
        newdf = pd.concat([commentdf, dflistforlabel], axis=1)
        
        #Part 3: for Tweets
        c = twint.Config()
        c.Search = text
        c.Limit = number
        c.Pandas = True
        #c.Since 
        #c.Until
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df.head(number)
        necessary_text = Tweets_df.tweet
        necessary_date = Tweets_df.date
        necessary_likes = Tweets_df.nlikes
        necessary_retweets = Tweets_df.nretweets
        necessarylinks= Tweets_df.link
        tweetlabel = ['Tweet'] * len(necessary_text)
        tweforlabel = pd.Series(tweetlabel)
        lastlabel = pd.concat([necessary_text, necessary_date], axis=1)
        finallabel = pd.concat([lastlabel,tweforlabel], axis = 1)
        otherlabel = pd.concat([necessarylinks, finallabel], axis = 1)
        otherlabel.rename(columns = {"link":"URL","tweet":"Text","date":"Date"}, inplace = True)
        final2label = pd.concat([otherlabel, necessary_likes], axis=1)
        final3label = pd.concat([final2label, necessary_retweets], axis=1)
        
        #Combine Part 1, Part 2, Part 3
        result1 = upnewdf.append(newdf, sort=False)
        result = result1.append(final3label,sort=False)
        result.columns = ["URL","Text","Date","Score", "Upvote Ratio", "Type","Likes","Retweets"]
        # Specify symbols to keep in text
        symbols_to_keep = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM:;!-,?.@ \n\"\'"
    
        # Function for removing unknown characters
        remove_unknown_chars = lambda x: ''.join(char for char in x if char in symbols_to_keep)
        # Function for removing all Twitter user tags (@ongunuzaymacar, etc.)
        remove_user_tags = lambda x: re.sub(r'@\w+', '', x)
        # Function for removing all Twitter hashtags (#freetheworld, ect.)
        remove_hash_tags = lambda x: re.sub(r'#\w+', '', x)
        # Function for removing all URLs (www.google.com, etc.)
        remove_urls = lambda x: re.sub(r'(https://|www.)[A-Za-z0-9_.]+', '', x)
        
        def clean_tweets(twoot): #cleaning text
            # Convert to lowercase and remove spaces from beginning
            twoot = str(twoot).lstrip()
            # Remove Twitter-related data
            twoot = remove_user_tags(twoot)
            twoot = remove_urls(twoot)
            twoot = remove_hash_tags(twoot)
            # Remove unwanted characters
            twoot = remove_unknown_chars(twoot)
            # Remove spaces from end and condense multiple spaces into one
            twoot = twoot.rstrip()
            twoot = re.sub(' +', ' ', twoot)
            return twoot
        result["Text"] = result["Text"].apply(clean_tweets)
        f = lambda x: " ".join(x["Text"].split())
        result["Text"] = result.apply(f, axis=1)
        
        def ner(x):
            nlp = spacy.load("en_core_web_md")
            doc = nlp(x)
            textually = []
            tags = []
            for ent in doc.ents:
                textually.append(ent.text)
                tags.append(ent.label_)
            spacy_dictionary = dict(zip(textually,tags))
            good_terms = []
            for key in spacy_dictionary:
                if spacy_dictionary[key] == "ORG":
                    good_terms.append(key)
                if spacy_dictionary[key] == "GPE":
                    good_terms.append(key)
                if spacy_dictionary[key] == "LOC":
                    good_terms.append(key)
                if spacy_dictionary[key] == "PRODUCT":
                    good_terms.append(key)
                if spacy_dictionary[key] == "DATE":
                    good_terms.append(key)
                if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                    good_terms.clear()
                return good_terms
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    def spacysmscraper(text,number):   
        nest_asyncio.apply()
        #Part 1: for Reddit threads
        reddit = praw.Reddit(client_id='x6e1LTj2OQnGYw', 
                         client_secret='cKPjQfnskfy1w5IlwLi6Aos-DMU', 
                         user_agent='trialnew', 
                         username='opposity', 
                         password='Samborules123?') 
        all = reddit.subreddit("technology+tech+futurology+engineering+army+navy+airforce+geek+military+scifi+science")
        topics_dict = { "URL":[],"Text":[], "Date":[],"Score":[],"Upvote_Ratio":[]}
        for submission in all.search(text, limit = number):
            topics_dict["URL"].append(submission.url)
            topics_dict["Text"].append(submission.title)
            topics_dict["Date"].append(submission.created_utc)
            topics_dict["Score"].append(submission.score)
            topics_dict["Upvote_Ratio"].append(submission.upvote_ratio)
        topics_data = pd.DataFrame(topics_dict)
        topics_data['Date'] = (pd.to_datetime(topics_data['Date'], unit='s'))
        listeforlabel = ['Reddit Thread'] * number
        dflisteforlabel = pd.Series(listeforlabel)
        upnewdf = pd.concat([topics_data, dflisteforlabel], axis=1)
    
        #Part 2: for Reddit comments
        subbies = ["technology","tech","futurology","engineering","army","navy","airforce","geek","military","scifi","science"]
        api = PushshiftAPI()
        gen = api.search_comments(q = text, subreddit = subbies)
        cache = []
        for c in gen:
            cache.append(c)
            if len(cache) >= number:
                break
        comments_df = pd.DataFrame([thing.d_ for thing in cache])
        commentdf = comments_df[["body","created","score","subreddit"]]
        commentdf.columns=["Text","Date","Score","URL"]
        commentdf['URL'] = 'https://www.reddit.com/r/' + commentdf['URL'].astype(str)
        commentdf['Date'] = (pd.to_datetime(commentdf['Date'], unit='s', errors = "coerce"))
        listforlabel = ['Reddit Comment'] * number
        dflistforlabel = pd.Series(listforlabel)
        newdf = pd.concat([commentdf, dflistforlabel], axis=1)
        
        #Part 3: for Tweets
        c = twint.Config()
        c.Search = text
        c.Limit = number
        c.Pandas = True
        #c.Since 
        #c.Until
        twint.run.Search(c)
        Tweets_df = twint.storage.panda.Tweets_df.head(number)
        necessary_text = Tweets_df.tweet
        necessary_date = Tweets_df.date
        necessary_likes = Tweets_df.nlikes
        necessary_retweets = Tweets_df.nretweets
        necessarylinks= Tweets_df.link
        tweetlabel = ['Tweet'] * len(necessary_text)
        tweforlabel = pd.Series(tweetlabel)
        lastlabel = pd.concat([necessary_text, necessary_date], axis=1)
        finallabel = pd.concat([lastlabel,tweforlabel], axis = 1)
        otherlabel = pd.concat([necessarylinks, finallabel], axis = 1)
        otherlabel.rename(columns = {"link":"URL","tweet":"Text","date":"Date"}, inplace = True)
        final2label = pd.concat([otherlabel, necessary_likes], axis=1)
        final3label = pd.concat([final2label, necessary_retweets], axis=1)
        
        #Combine Part 1, Part 2, Part 3
        result1 = upnewdf.append(newdf, sort=False)
        result = result1.append(final3label,sort=False)
        result.columns = ["URL","Text","Date","Score", "Upvote Ratio", "Type","Likes","Retweets"]
        result = result[['Text', 'Type','Date', 'Score', 'Upvote Ratio', 'Likes','Retweets','URL']]
        # Specify symbols to keep in text
        symbols_to_keep = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM:;!-,?.@ \n\"\'"
    
        # Function for removing unknown characters
        remove_unknown_chars = lambda x: ''.join(char for char in x if char in symbols_to_keep)
        # Function for removing all Twitter user tags (@ongunuzaymacar, etc.)
        remove_user_tags = lambda x: re.sub(r'@\w+', '', x)
        # Function for removing all Twitter hashtags (#freetheworld, ect.)
        remove_hash_tags = lambda x: re.sub(r'#\w+', '', x)
        # Function for removing all URLs (www.google.com, etc.)
        remove_urls = lambda x: re.sub(r'(https://|www.)[A-Za-z0-9_.]+', '', x)
        
        def clean_tweets(twoot):
            # Convert to lowercase and remove spaces from beginning
            twoot = str(twoot).lstrip()
            # Remove Twitter-related data
            twoot = remove_user_tags(twoot)
            twoot = remove_urls(twoot)
            twoot = remove_hash_tags(twoot)
            # Remove unwanted characters
            twoot = remove_unknown_chars(twoot)
            # Remove spaces from end and condense multiple spaces into one
            twoot = twoot.rstrip()
            twoot = re.sub(' +', ' ', twoot)
            return twoot
        result["Text"] = result["Text"].apply(clean_tweets)
        f = lambda x: " ".join(x["Text"].split())
        result["Text"] = result.apply(f, axis=1)
        
        def ner(x):
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(x)
            textually = []
            tags = []
            for ent in doc.ents:
                textually.append(ent.text)
                tags.append(ent.label_)
            spacy_dictionary = dict(zip(textually,tags))
            good_terms = []
            for key in spacy_dictionary:
                if spacy_dictionary[key] == "ORG":
                    good_terms.append(key)
                if spacy_dictionary[key] == "GPE":
                    good_terms.append(key)
                if spacy_dictionary[key] == "LOC":
                    good_terms.append(key)
                if spacy_dictionary[key] == "PRODUCT":
                    good_terms.append(key)
                if spacy_dictionary[key] == "DATE":
                    good_terms.append(key)
                if ("PRODUCT" not in spacy_dictionary.values()) and ("ORG" not in spacy_dictionary.values()):
                    good_terms.clear()
                return good_terms
        result.drop_duplicates(subset ="Text", 
                     keep = False, inplace = True) 
        result =  result[result['Text'].str.contains('[A-Za-z]')]
        result["NER Model"] = result["Text"].apply(ner)
        result['Sentiment'] = result.Text.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        result['Subjectivity'] = result.Text.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return result
    if method == "Social_Media_Spacy_SM":
        return spacysmscraper(text,number)
    if method == "Social_Media_Spacy_MD":
        return spacymdscraper(text,number)
    if method == "Magazines_Spacy_SM":
        return spacy_sm_magazine_scraper(text,number)
    if method == "Magazines_Spacy_MD":
        return spacy_md_magazine_scraper(text,number)
    if method == "Social_Media_Deep_Pavlov":
        return deeppavlovscraper(text,number)
    if method == "Magazines_Deep_Pavlov":
        return deeppavlov_magazine_scraper(text,number)
    
def secondaryscraper(text,number,method):
    def arxivscraping(text,number):    
        feed = feedparser.parse(f"http://export.arxiv.org/api/query?search_query=all:{text}&start=0&max_results={number}")
        feed_dict = { "Title":[], "Date":[],"Summary":[],"Author":[],"Link":[]}
        for post in feed.entries:
            feed_dict["Title"].append(post.title)
            feed_dict["Date"].append(post.published)
            feed_dict["Summary"].append(post.summary)
            feed_dict["Author"].append(post.author)
            feed_dict["Link"].append(post.id)
        
        deef = pd.DataFrame(feed_dict)
        deeflabel = ['Academia'] * len(deef)
        deefforlabel = pd.Series(deeflabel)
        newdeef = pd.concat([deef,deefforlabel], axis = 1)
        newdeef.columns = ["Title","Date","Summary","Author","Link","Type"]
        newdeef['Sentiment'] = newdeef.Summary.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        newdeef['Subjectivity'] = newdeef.Summary.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return newdeef
    def uspatent(text,number):
        driver = webdriver.Chrome('./chromedriver')
        conn = pypatent.WebConnection(use_selenium=True, selenium_driver = driver)
        x = pypatent.Search(text, results_limit=number, get_patent_details=False, web_connection=conn).as_dataframe()
        xlabel = ['Patent'] * len(x)
        xforlabel = pd.Series(xlabel)
        newx = pd.concat([x,xforlabel], axis = 1)
        newx.columns = ["Title","URL","Type"]
        newx['Sentiment'] = newx.Title.apply(lambda x: TextBlob(str(x)).sentiment.polarity)
        newx['Subjectivity'] = newx.Title.apply(lambda x:TextBlob(str(x)).sentiment.subjectivity)
        return newx
    
    if method == "Patent":
        return uspatent(text,number)
    else:
        return arxivscraping(text,number)


@Gooey(
       program_name="ASA ALT Scraper",
       menu=[{
           'name': 'Help',
           'items': [{
                'type': 'Link',
                'menuTitle': 'Example Usage',
                'url': 'https://streamable.com/7iy2hd'
            }, {
                'type': 'Link',
                'menuTitle': 'Documentation',
                'url': 'https://docdro.id/7RUMEct'
            },
                {
                'type': 'Link',
                'menuTitle': 'Source Code Explanation',
                'url': 'https://youtu.be/0YHl0etXHmo'
            },{
                'type': 'Link',
                'menuTitle': 'About the developer',
                'url': 'https://www.linkedin.com/in/kerem-tuncer-b7a594106/'}]}],image_dir=r"C:\Users\Kerem's Laptop\Documents")
def main():
    desc = "Project for CTO of ASA ALT"
    parser = GooeyParser(description=desc)
    subparsers = parser.add_subparsers(help='options', dest='subparser_name')
    main_parser = subparsers.add_parser('Primary')
    mag_parser = subparsers.add_parser('Secondary')
    primary_fields = main_parser.add_argument_group('Primary parameters')
    secondary_fields = mag_parser.add_argument_group('Secondary parameters')
    primary_fields.add_argument(
        "--Text", action="store", help="Keyword to search")
    primary_fields.add_argument(
        "--Number", action="count", help="Output Amount")
    primary_fields.add_argument(
        '--Method', choices=['Social_Media_Spacy_SM', 'Social_Media_Spacy_MD','Social_Media_Deep_Pavlov','Magazines_Spacy_SM','Magazines_Spacy_MD',"Magazines_Deep_Pavlov"], help='Pick usage')
    secondary_fields.add_argument(
        "--Keyword", action="store", help="Output Keyword")
    secondary_fields.add_argument(
        "--Amount", action="count", help="Output Amount")
    secondary_fields.add_argument(
        "--Platform", choices = ["Academia"], help="Output Platform")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = main()
    if args.subparser_name == 'Primary':
        #print(ultimategrabber(args.Text, args.Number,args.Method))
        
        df=ultimategrabber(args.Text, args.Number,args.Method)
        labels = list(df['Type'].unique())
        values = []
        if "Reddit Thread" in labels:
            values.append((len(df[df['Type'].str.contains('Reddit Thread')])))
        if "Reddit Comment" in labels:
            values.append((len(df[df['Type'].str.contains('Reddit Comment')])))
        if "Tweet" in labels:
            values.append((len(df[df['Type'].str.contains('Tweet')])))
        if "IEEE" in labels:
            values.append((len(df[df['Type'].str.contains('IEEE')])))
        if "PopScience" in labels:
            values.append((len(df[df['Type'].str.contains('PopScience')])))
        if "Wired" in labels:
            values.append((len(df[df['Type'].str.contains('Wired')])))
        if "Scientific American" in labels:
            values.append((len(df[df['Type'].str.contains('Scientific American')])))
        if "Science Mag" in labels:
            values.append((len(df[df['Type'].str.contains('Science Mag')])))
        if "MIT Tech Review" in labels:
            values.append((len(df[df['Type'].str.contains('MIT Tech Review')])))
        if "American Scientist" in labels:
            values.append((len(df[df['Type'].str.contains('American Scientist')])))
        if "New Scientist" in labels:
            values.append((len(df[df['Type'].str.contains('New Scientist')])))
        if "ScienceNews" in labels:
            values.append((len(df[df['Type'].str.contains('ScienceNews')])))
    
        polmean = df["Sentiment"].mean()
        submean = df["Subjectivity"].mean()
        
        
        fig = go.Figure(data = [go.Pie(labels=labels, values=values)], layout = {
                        "margin": dict(l=20, r=20, t=20, b=20),
                        "showlegend": True,
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "font": {"color": "white"},
                        "autosize": True,
                    })
        
        
        app.layout = html.Div(
            [
                # header
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("ASA ALT Technology Search Engine", className="app__header__title"),
                                html.P(
                                    "This app can be used for identification and evaluation of emerging STEM technologies through social media",
                                    className="app__header__title--grey",
                                ),
                            ],
                            className="app__header__desc",
                        ),
                        html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url("logo.png"),
                                    className="app__menu__img",
                                )
                            ],
                            className="app__header__logo",
                        ),
                    ],
                    className="app__header",
                ),
                html.Div(
                    [
                        # wind speed
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("RESULTS", className="graph__title")]
                                ),
                                dash_table.DataTable(
                                id='table',
                                   style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'font-family':'Verdana',
                                       'backgroundColor': 'rgb(8, 34, 85)',
                'color': 'white'},
                                columns=[{"name": i, "id": i} for i in df.columns],
                                data=df.to_dict('records'),
                                sort_action='native',
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(8, 34, 85)'
                                    }
                                ],
                                style_header={
                                    'backgroundColor': 'rgb(6, 30, 68)',
                                    'fontWeight': 'bold'
                                },
                                style_table={'overflowX': 'auto'}),
                                dcc.Interval(
                                    id="wind-speed-update",
                                    interval=int(GRAPH_INTERVAL),
                                    n_intervals=0,
                                ),
                            ],
                            className="two-thirds column wind__speed__container",
                        ),
                        html.Div(
                            [
                                # histogram
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    "PLATFORMS",
                                                    className="graph__title",
                                                )
                                            ]
                                        ),
        
                                        dcc.Graph(
                id='example-graph-2',
                figure=fig
            ),
                                    ],
                                    className="graph__container first",
                                ),
                                # wind direction
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    "POLARITY AND SUBJECTIVITY", className="graph__title"
                                                )
                                            ]
                                        ),
                                        dcc.Graph(
                id='example-graph',
        
                figure={
                    'data': [
                        {'x': [1], 'y': [polmean
        ], 'type': 'bar', 'name': 'Polarity'},
                        {'x': [1], 'y': [submean
        ], 'type': 'bar', 'name': 'Subjectivity'},
                    ],
                    'layout': {
                        'paper_bgcolor': "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "font": {"color": "white"},
                    }
                }
            ),
                                    ],
                                    className="graph__container second",
                                ),
                            ],
                            className="one-third column histogram__direction",
                        ),
                    ],
                    className="app__content",
                ),
            ],
            className="app__container",
        )
        
        
        
        app.run_server(debug=False)
    elif args.subparser_name == 'Secondary':
        bdf = secondaryscraper(args.Keyword, args.Amount,args.Platform)
        newlabels = list(bdf['Type'].unique())
        newvalues = []
        if "Academia" in newlabels:
            newvalues.append((len(bdf[bdf['Type'].str.contains('Academia')])))
        if "Patent" in newlabels:
            newvalues.append((len(bdf[bdf['Type'].str.contains('Patent')])))
        newpolmean = bdf["Sentiment"].mean()
        newsubmean = bdf["Subjectivity"].mean()
        newfig = go.Figure(data = [go.Pie(labels=newlabels, values=newvalues)], layout = {
                        "margin": dict(l=20, r=20, t=20, b=20),
                        "showlegend": True,
                        "paper_bgcolor": "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "font": {"color": "white"},
                        "autosize": True,
                    })
        
        app.layout = html.Div(
            [
                # header
                html.Div(
                    [
                        html.Div(
                            [
                                html.H4("ASA ALT Technology Search Engine", className="app__header__title"),
                                html.P(
                                    "This app can be used for identification and evaluation of emerging STEM technologies through social media",
                                    className="app__header__title--grey",
                                ),
                            ],
                            className="app__header__desc",
                        ),
                        html.Div(
                            [
                                html.Img(
                                    src=app.get_asset_url("logo.png"),
                                    className="app__menu__img",
                                )
                            ],
                            className="app__header__logo",
                        ),
                    ],
                    className="app__header",
                ),
                html.Div(
                    [
                        # wind speed
                        html.Div(
                            [
                                html.Div(
                                    [html.H6("RESULTS", className="graph__title")]
                                ),
                                dash_table.DataTable(
                                id='table',
                                   style_cell={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                    'font-family':'Verdana',
                                       'backgroundColor': 'rgb(8, 34, 85)',
                'color': 'white'},
                                columns=[{"name": i, "id": i} for i in bdf.columns],
                                data=bdf.to_dict('records'),
                                sort_action='native',
                                filter_action='native',
                                style_data_conditional=[
                                    {
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(8, 34, 85)'
                                    }
                                ],
                                style_header={
                                    'backgroundColor': 'rgb(6, 30, 68)',
                                    'fontWeight': 'bold'
                                },
                                style_table={'overflowX': 'auto'}),
                                dcc.Interval(
                                    id="wind-speed-update",
                                    interval=int(GRAPH_INTERVAL),
                                    n_intervals=0,
                                ),
                            ],
                            className="two-thirds column wind__speed__container",
                        ),
                        html.Div(
                            [
                                # histogram
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    "PLATFORMS",
                                                    className="graph__title",
                                                )
                                            ]
                                        ),
        
                                        dcc.Graph(
                id='example-graph-2',
                figure=newfig
            ),
                                    ],
                                    className="graph__container first",
                                ),
                                # wind direction
                                html.Div(
                                    [
                                        html.Div(
                                            [
                                                html.H6(
                                                    "POLARITY AND SUBJECTIVITY", className="graph__title"
                                                )
                                            ]
                                        ),
                                        dcc.Graph(
                id='example-graph',
        
                figure={
                    'data': [
                        {'x': [1], 'y': [newpolmean
        ], 'type': 'bar', 'name': 'Polarity'},
                        {'x': [1], 'y': [newsubmean
        ], 'type': 'bar', 'name': 'Subjectivity'},
                    ],
                    'layout': {
                        'paper_bgcolor': "rgba(0,0,0,0)",
                        "plot_bgcolor": "rgba(0,0,0,0)",
                        "font": {"color": "white"},
                    }
                }
            ),
                                    ],
                                    className="graph__container second",
                                ),
                            ],
                            className="one-third column histogram__direction",
                        ),
                    ],
                    className="app__content",
                ),
            ],
            className="app__container",
        )
        app.run_server(debug=False)
        
        
        
