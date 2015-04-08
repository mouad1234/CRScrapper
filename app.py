import requests
import re
import webbrowser

def main():
    r = requests.get("http://www.crunchyroll.com/bleach/episode-364-untitled-588342")
    showList = printShows()
    id =raw_input("Enter Series ID: ")
    seriesName = selectShow(showList, id)
    episodeNbr = raw_input("Episode number: ")
    episodeList = getVidList(seriesName)
    url = urlSelector(episodeNbr,episodeList)
    openShow(url)

def selectShow(showList, id):
    id = int(id)
    return showList[id].urlName

def openShow(url):
    if url != "":
        http = requests.get("http://www.crunchyroll.com" + url)
        req = vidSourcefromURL(http)
        print "The url is: " + req
        webOpen = raw_input("Do you want to open the page? (Y/N): ")
        if webOpen == "Y":
            webbrowser.open(req)
        else:
            print "Operation Aborted"
    else:
        print "Cannot find episode"


def printShows():
    Shows = []
    kuroko = Show("Kuroko's Basketball", "kurokos-basketball")
    bleach = Show("Bleach", "bleach")
    Shows.append(kuroko)
    Shows.append(bleach)
    i = 0
    for show in Shows:
        print show, i
        i +=1
    return Shows


class Show:
    name = ""
    urlName =""
    def __init__(self, name, urlName):
        self.name = name
        self.urlName = urlName
    def __str__(self):
        return self.name

def urlSelector(input, episodeList):
    for episode in episodeList:
        if episode.find("episode-" + input + "-") >= 0:
            return episode
    return ""


def vidSourcefromURL(r):
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

def getVidList(seriesName):
    req = requests.get("http://www.crunchyroll.com/" + seriesName)
    r = req.text
    p = re.compile(ur'"(.*?)"')
    list = re.findall(p,r)
    epList = []
    for element in list:
        if element.find("/" + seriesName + "/episode-") >=0:
            epList.append(element)
    return epList


def showsGrabber():
    req = requests.get("http://www.crunchyroll.com/videos/anime")
    r = req.text
    #print req.text
    p = re.compile(ur'(token="shows-portraits" itemprop="url" href=)"(.*)" (class)')
    list = re.findall(p,r)
    for element in list:
        print element[1]

main()
