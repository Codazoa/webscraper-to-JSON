#!/usr/bin/python3

# setting up imports
import os
import sys
from bs4 import BeautifulSoup
from lxml import etree
import requests
import re

def setAction(whatAction):
    """ Setting up action for api call """
    return 'action='+whatAction+'&'

def setFormat(whatFormat):
    """ Setting up format for api call """
    return 'format='+whatFormat+'&'

def searchFor(searchTerms, limit):
    """ Setting up terms for search api call """
    return 'search='+searchTerms+'&limit='+limit+'&'

def titles(whatTitles):
    """ Setting up titles for query api call """
    listOfTitles = ''
    for title in whatTitles:
        listOfTitles += title+"|"
    return 'titles='+listOfTitles[:-1]+'&'

def getPage(url):
    """ Returns page contents for given url """
    page = requests.get(url)
    return page

def searchWikiURL(wikiURL, searchTerms, limit):
    """ Runs a search api call """
    return wikiURL+setAction('opensearch')+setFormat('xml')+searchFor(searchTerms, limit)

def queryWikiURL(wikiURL, queryTerms):
    """ Runs a query api call """
    return wikiURL+setAction('query')+setFormat('xml')+titles(queryTerms)

def strip_ns(tree):
    """ Strips namespace from xml output """
    for node in tree.iter():
        try:
            has_namespace = node.tag.startswith('{')
        except AttributeError:
            continue
        if has_namespace:
            node.tag = node.tag.split('}', 1)[1]

def getLinkList(url):
    """ finds all the links on a page and appends them to a list
        from cs224 programer tools assignment
    """
    page = BeautifulSoup(requests.get(url).text, 'html.parser')
    body = page.find(id="bodyContent")
    list = []
    for link in body.find_all('a', href=filterLinks):
        list.append('https://en.wikipedia.org' + link.get('href'))
    return list

def filterLinks(href):
    """ returns true if href is an internal link in wikipedia, false if not
        from cs224 programer tools assignment
    """
    if href:
        if re.compile('^/wiki/').search(href):
            if not re.compile('/\w+:').search(href):
                if not re.compile('#').search(href):
                    return True
    return False

def main():
    # startingUrl = 'https://en.wikipedia.org/wiki/Lists_of_video_games'

    # links = getLinkList(startingUrl)
    # for link in links:
    #     print(link)

    wiki = "https://en.wikipedia.org/w/api.php?"
    url = queryWikiURL(wiki, ['Gex (video game)'])
    print(url)
    rawPage = getPage(url)
    print(rawPage.text)



    # rawPage = getPage(wikiURL)
    # print(rawPage.text)

    pass


if __name__ == '__main__':
    main()
