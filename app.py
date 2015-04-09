import requests
import re
import webbrowser
import sys
sys.path.append("crunchy-xml-decoder/")
from ultimate import *

def main():
    method_selector = raw_input("Select show by ID [0] or search for show [1] ?: ")
    show_list = show_grabber()
    if method_selector == "0":
        print_shows(show_list)
        id =raw_input("Enter Series ID: ")
    elif method_selector == "1":
        show_list = show_grabber()
        query = raw_input("Enter query: ")
        show_list = search_show(query, show_list)
        print_shows(show_list)
        id =raw_input("Enter Series ID: ")
    else:
        return
    name = select_show(show_list, id)
    episode_list = get_vid_list(name)
    episode_nbr = raw_input("Episode number: ")
    url = url_selector(episode_nbr, episode_list)
    open_show(url)
    res = raw_input("To restart press Y, otherwise press any other key: ")
    if res == "Y" or res == "y":
        main()
    else:
        exit()


def search_show(query, show_list):
    search_result = []
    for show in show_list:
        if show.name.lower().find(query.lower()) > -1:
            search_result.append(show)
    return search_result


def select_show(show_list, id):
    id = int(id)
    return show_list[id].url_name


def open_show(url):
    if url != "":
        http = requests.get("http://www.crunchyroll.com" + url)
        selector = raw_input("Download (PC Only) [0] or Stream Online[1]: ")
        if selector == '0':
            start(url)
        elif selector == '1':
            req = vid_source_from_url(http)
            webbrowser.open(req)
        else:
            print "Operation Aborted, Invalid Input"
    else:
        print "Cannot find episode"


def print_shows(shows):
    i = 0
    for show in shows:
        print show, "["+str(i)+"]"
        i +=1


class Show:
    name = ""
    url_name = ""

    def  __init__(self, name, urlname):
        self.name = name
        self.url_name = urlname

    def __str__(self):
        return self.name

def url_selector(input_url, episode_list):
    for episode in episode_list:
        if episode.find("episode-" + input_url + "-") >= 0:
            return episode
    return ""


def vid_source_from_url(r):
    http = r.text
    index = http.find("video_src")
    http = http[index-11:]
    index2 = http.find("/>")
    http= http[:index2+2]
    index3 = http.find("http")
    http = http[index3:]
    index4 = http.find("/>")
    http = http[:index4-2]
    return http

def get_vid_list(series_name):
    req = requests.get("http://www.crunchyroll.com/" + series_name)
    r = req.text
    p = re.compile(ur'"(.*?)"')
    list = re.findall(p,r)
    ep_list = []
    for element in list:
        if element.find("/" + series_name + "/episode-") >=0:
            ep_list.append(element)
    print len(ep_list), "Episodes available"
    return ep_list


def show_grabber():
    req = requests.get("http://www.crunchyroll.com/videos/anime/alpha?group=all")
    r = req.text
    p = re.compile(ur'(token="shows-portraits" itemprop="url" href=)"(.*)" (class)')
    list = re.findall(p, r)
    show_list = []
    for element in list:
        # Converts Tuple to String, removes "-" and joins them with " "
        title = str(element[1]) 
        title = " ".join(title[1:].split("-")) 
        title = title[0].capitalize() + title[1:]
        url_name = str(element[1])[1:]
        show_list.append(Show(title, url_name))
    return show_list

main()