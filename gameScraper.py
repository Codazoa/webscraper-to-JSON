#!/usr/bin/python3

# Name: Cody Vernon
# CS454 Information Retrieval web scraper
#

# setting up imports
import os
import sys
from bs4 import BeautifulSoup
import json
import requests
import pandas as pd
import re
import time

class JSONRunner:
    def __init__(self, filename):
        self.jsonFileName = filename
        self.jsonHeading = 'webdata' # label for the json section
        self.titleList = [] # keep track of files already stored in json

    def __createJson(self, filename):
        if not os.path.exists(filename): # if file doesnt already exist create it with a blank json field
            with open(filename, "x") as newfile:
                jsonDict = { self.jsonHeading : []} # create initial json dict object
                json.dump(jsonDict, newfile, indent = 2) # dump dict contents into the json file

    def writeToJson(self, data):
        filename = self.jsonFileName

        # check if the json file exists and create it if not
        if not os.path.exists(filename):
            self.__createJson('webdata.json')

        with open(filename, 'r+') as outfile:
            file_data = json.load(outfile) # load json data into python dict
            file_data[ self.jsonHeading ].append(data) # append new dict entry
            outfile.seek(0) # reset file pointer to beginning of file
            json.dump(file_data, outfile, indent = 2) # dump new json data back into file


class WebScraper (object):
    def __init__(self, startingUrl):
        self.startingUrl = startingUrl # Url of list to start at
        self.wiki = "https://en.wikipedia.org/w/api.php?"
        self.jsonWriter = JSONRunner("webdata.json")

    def setAction(self, whatAction):
        return 'action='+whatAction+'&'

    def setFormat(self, whatFormat):
        return 'format='+whatFormat+'&'

    def searchFor(self, searchTerms, limit):
        return 'search='+searchTerms+'&limit='+limit+'&'

    def titles(self, title):
        return 'titles='+ title +'&'

    def getLinkList(self, url):
        """ finds all the links on a page and appends them to a list
            from cs224 programming tools assignment
        """
        page = BeautifulSoup(requests.get(url).text, 'html.parser')
        body = page.find(id="bodyContent")
        list = []
        for link in body.find_all('a', href=self.filterLinks):
            list.append('https://en.wikipedia.org' + link.get('href'))
        return list

    def filterLinks(self, href):
        """ returns true if href is an internal link in wikipedia, false if not
            from cs224 programming tools assignment
        """
        if href:
            if re.compile('^/wiki/').search(href):
                if not re.compile('/\w+:').search(href):
                    if not re.compile('#').search(href):
                        return True
        return False

    def getPage(self, url):
        page = requests.get(url)
        return page

    def searchWikiURL(self, wikiURL, searchTerms, limit):
        return wikiURL+self.setAction('opensearch')+self.setFormat('json')+self.searchFor(searchTerms, limit)

    def queryWikiURL(self, wikiURL, queryTerms):
        return wikiURL+self.setAction('query')+"prop=extracts&"+self.setFormat('json')+self.titles(queryTerms)

    def getTitleList(self, url):
        titles = []
        data = pd.read_html(url) # load table into pandas object

        # parse though tables for ones that contain "Title"
        for table in data:
            if "Title" in table.columns:
                #add titlesfrom table into title list
                titles = titles + table.Title.to_string(index=False).splitlines()

        titles = [name.strip() for name in titles] # strip leading whitespace from titles

        # remove first "title" entry in list
        if len(titles) > 0:
            titles.pop(0)
        return titles

    def getUrl(self, title):
        # request json data from api and load it into the dictionary
        dict = json.loads(self.getPage(self.searchWikiURL(self.wiki, title, '1')).text)
        return dict[3][0] # parse json to get url for title

    def getImageUrl(self, title):
        url = self.getUrl(title) # get the url for the title
        page = BeautifulSoup(requests.get(url).text, 'html.parser') #set up html parser on page
        image = page.find_all('img') # find all the images on current page

        # check to see that there was an image found
        if len(image) > 0:
            return image[0]['src'][2:] # return the first image found
        return "" # otherwise return emtpy string

    def collectData(self, topic):
        print(f'Scraping data for {topic} from {self.startingUrl}')
        # find all links in list that contain topic word
        links = self.getLinkList(self.startingUrl)
        topicLinks = [] # list to hold links for our topic

        # find only links that pertain to the topic
        for link in links:
            if topic in link.lower() and "list" in link.lower():
                topicLinks.append(link)
        # topicLinks now has only links with [topic] and list in the name

        # go into each list to find the contained titles
        for link in topicLinks:
            titleList = self.getTitleList(link) # get a list of game titles to query

            for title in titleList: # query each title
                time.sleep(2) #sleep for a little bit so we don't upset the api

                if title in self.jsonWriter.titleList: # don't perform scraping if we have seen title before
                    continue

                self.jsonWriter.titleList.append(title) # add current title to json title list

                rawJson = self.getPage(self.queryWikiURL(self.wiki, title)).text # get the raw json data from api call

                jsonDict = json.loads(rawJson) # load the json as a dictionary
                jsonDict = jsonDict['query']['pages'] # set jsonDict as a subkey of the original
                pageId = list(jsonDict)[0] # get the page Id to decend into next key

                if pageId == '-1': # if page doesn't exist go to next title
                    continue

                jsonDict = jsonDict[pageId] # decend into final section of json data

                content = jsonDict['extract'] # grab extract for content
                contentUrl = self.getUrl(title) # grab the url for the current title
                image = self.getImageUrl(title) # grab url for box art image for title

                # hit a parsing limit, we can leave this one out for now
                if "NewPP limit report" in content:
                    continue

                print(f'\nFound {title}\nFound {image}\n')

                # create dict object to dump into json
                newDataDict =   { 'title': title,
                                  'url': contentUrl,
                                  'image': image,
                                  'content': content
                                }

                self.jsonWriter.writeToJson(newDataDict) # write the new data to the database


def main(argv = sys.argv[1:]):

    # error check argument number
    if len(argv) != 1:
        raise Exception("Incorrect number of arguments\nCorrect form:\npython3 gameScraper.py [gameConsole]")

    # set up scraper and start collection
    scraper = WebScraper('https://en.wikipedia.org/wiki/Lists_of_video_games')
    scraper.collectData(argv[0])


if __name__ == '__main__':
    main()
