import requests
import re
import webbrowser
import sys
sys.path.append("crunchy-xml-decoder/")
from ultimate import *

def main():
    r = requests.get("http://www.crunchyroll.com/bleach/episode-364-untitled-588342")
    showList = printShows()
    id =raw_input("Enter Series ID: ")
    name = selectshow(showList, id)
    episodeNbr = raw_input("Episode number: ")
    episodeList = getvidlist(name)
    url = urlselector(episodeNbr, episodeList)
    openshow(url)


def selectshow(showlist, id):
    id = int(id)
    return showlist[id].urlname


def openshow(url):
    if url != "":
        http = requests.get("http://www.crunchyroll.com" + url)
        selector = raw_input("Download (0) or Stream Online(1): ")
        if selector == '0':
            start(url)
        elif selector == '1':
            req = vidsourcefromurl(http)
            webbrowser.open(req)
        else:
            print "Operation Aborted, Invalid Input"
    else:
        print "Cannot find episode"


def printShows():
    shows = showsgrabber()
    i = 0
    for show in shows:
        print show, i
        i +=1
    return shows


class Show:
    name = ""
    urlname =""
    def __init__(self, name, urlname):
        self.name = name
        self.urlname = urlname
    def __str__(self):
        return self.name

def urlselector(input, episodelist):
    for episode in episodelist:
        if episode.find("episode-" + input + "-") >= 0:
            return episode
    return ""


def vidsourcefromurl(r):
    http = r.text
    index = http.find("video_src")
    http = http[index-11:]
    index2 = http.find("/>")
    http= http[:index2+2]
    index3 = http.find("http")
    http = http[index3:]
    index4 = http.find("/>")
    http = http[:index4-2]
    req = requests.get(http)
    return http

def getvidlist(seriesname):
    req = requests.get("http://www.crunchyroll.com/" + seriesname)
    r = req.text
    p = re.compile(ur'"(.*?)"')
    list = re.findall(p,r)
    eplist = []
    for element in list:
        if element.find("/" + seriesname + "/episode-") >=0:
            eplist.append(element)
    return eplist


def showsgrabber():
    req = requests.get("http://www.crunchyroll.com/videos/anime")
    r = req.text
    p = re.compile(ur'(token="shows-portraits" itemprop="url" href=)"(.*)" (class)')
    list = re.findall(p, r)
    showslist = []
    for element in list:
        # Converts Tuple to String, removes "-" and joins them with " "
        title = str(element[1]) 
        title = " ".join(title[1:].split("-")) 
        title = title[0].capitalize() + title[1:]
        urlName = str(element[1])[1:]
        showslist.append(Show(title, urlName))
    return showslist

main()