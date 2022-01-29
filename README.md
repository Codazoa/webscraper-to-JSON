# Webscraper-to-JSON
This script will scrape Wikipedia for the page content of every xbox branded game. The results will be stored in a json database with the form

```
{ "webdata": [
    {
      "title": "example"
      "url" : "www.example.com"
      "image": "www.example.com/someimage.png"
      "content": "This is the content of this particular example page"
    }
  ]
}
```

### Instructions to run
Be sure to have the dependencies installed prior to running this script
`python3 gameScraper.py [gameConsole]`

Example `python3 gameScraper.py xbox`

### Dependencies
BeautifulSoup4 `pip3 install BeautifulSoup4`\
Requests `pip3 install requests`\
Pandas `pip3 install pandas`
