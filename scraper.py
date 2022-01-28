#!/usr/bin/python3

# setting up imports
import os
import sys
from bs4 import BeautifulSoup
import json
import requests
import re

class JSONRunner (object):
    def __init__(self, filename):
        self.jsonFileName = filename
        self.jsonHeading = 'webdata'
        self.titleList = ''
        self.__createJson(self.jsonFileName)

    def __createJson(self, filename):
        with open(filename, "x") as newfile:
            jsonDict = { self.jsonHeading : []}
            print(jsonDict)
            json.dump(jsonDict, newfile, indent = 2)

    def writeToJson(self, data):
        filename = self.jsonFileName
        with open(filename, 'r+') as outfile:
            file_data = json.load(outfile)
            print(file_data)
            file_data[ self.jsonHeading ].append(data)
            outfile.seek(0)
            json.dump(file_data, outfile, indent = 2)


class WebScraper (object):
    def __init__(self, startingUrl):
        self.startingUrl = startingUrl

    def getLinkList(self, url):
        """ finds all the links on a page and appends them to a list
            from cs224 programming tools assignment
        """
        page = BeautifulSoup(requests.get(url).text, 'html.parser')
        body = page.find(id="bodyContent")
        list = []
        for link in body.find_all('a', href=filterLinks):
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

    def searchWikiURL(self, wikiURL, searchTerms, limit):
        return wikiURL+setAction('opensearch')+setFormat('xml')+searchFor(searchTerms, limit)

    def queryWikiURL(self, wikiURL, queryTerms):
        return wikiURL+setAction('query')+setFormat('xml')+titles(queryTerms)

def main():
    scraper = WebScraper('https://en.wikipedia.org/wiki/Lists_of_video_games')
    jsonwriter = JSONRunner("jsontest.json")


    # scraper code
    # search through the list
    # get title
    # check if title exists in our database
    # search title
    # get url
    # query title
    # get content
    #

    # rawPage = getPage(wikiURL)
    # print(rawPage.text)

    pass


if __name__ == '__main__':
    main()
