import requests
import re

def main():
    r = requests.get("http://www.crunchyroll.com/bleach/episode-364-untitled-588342")
    req = vidSourcefromURL(r)
    print req
    getVidList()

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

def getVidList():
    req = requests.get("http://www.crunchyroll.com/one-piece")
    r = req.text
    p = re.compile(ur'"(.*?)"')
    list = re.findall(p,r)
    for element in list:
        if element.find("/one-piece/episode-") >=0:
            print element
main()

