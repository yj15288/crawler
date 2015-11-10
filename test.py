import urllib
import urllib.request
import re
from collections import deque
from bs4 import BeautifulSoup
import os

def saveFile(data, fname):
    try:
        fobj = open(fname, 'w')
        fobj.write(data)
        fobj.close()
    except:
        return

#main
htmlpath = './pages/html/'
txtpath = './pages/txt/'
os.popen('rm -rf ' + htmlpath + '* ' + txtpath + '*')
mp = {}#map for title to url
queueurl = deque()#queue for BFS
queueurl.append('http://www.yahoo.com')
cnt = 0
visited = set()#set for visited url, to avoid duplicated visited
visited |= {'http://www.yahoo.com'}
while queueurl:
    if cnt > 99:
        break
    url = queueurl.popleft()
    #title = queuetitle.popleft()
    print(cnt, 'opening --->', url)
    try:
        data = urllib.request.urlopen(url, timeout=2).read().decode('UTF-8')
        soup = BeautifulSoup(data, 'lxml')
        title = soup.title.string
    except:
        continue
    urlList = re.findall('\"(http://.+?)\".+?title', data)

    #save html
    cnt = cnt + 1
    print(cnt, ' save---> ', title, url)
    #path could be changed
    htmlfnm = str(cnt) + '-' + title + '.html'
    saveFile(data, htmlpath + htmlfnm)
    mp[title] = url
    #handle html to avoid OneTwoThreeblablabla.....Explicitly...to avoid no space between words
    soup.title.append('\n')
    soup.title.insert_before(' ')
    scriptList = soup.find_all('script')
    styleList = soup.find_all('style')
    spanList = soup.find_all('span')
    aList = soup.find_all('a')
    iconList = soup.find_all(class_ = 'Icon')
    for scrptElement in scriptList:
        scrptElement.extract()
    for stlElement in styleList:
        stlElement.extract()
    for spanElement in spanList:
        spanElement.append(' ')
    for aElement in aList:
        aElement.append(' ')
    for iconElement in iconList:
        iconElement.extract()
    text = soup.get_text()
    txtfnm = str(cnt) + '-' + title +'.txt'
    saveFile(text, txtpath + txtfnm)
    #handle end
    for item in urlList:
        url = str(item)
        reForTitle = '\"' + url + '\".+?title=\"(.*?)\"'
        try:
            titlelst = re.findall(reForTitle, data)
        except:
            continue
        url.replace('/', '')#handle some bad url like "http:/\/\blabla..."the fucking '/' in url
        for item in titlelst:
            if str(item) is not '' and url not in visited:
                visited |= {url}
                queueurl.append(url)
                print('Enqueue--->', str(item), url)
#end main