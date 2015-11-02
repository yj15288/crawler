import urllib
import urllib.request
import re
from collections import deque

url = 'http://www.yahoo.com'
data = urllib.request.urlopen(url).read()
data = data.decode('UTF-8')

lst = re.findall('\"(http.+?)\".+?title', data)
print(lst)
mp = {}
for item in lst:
    url = str(item)
    objre = '''href=\"''' + url + '''\".+?title=\"(.*?)\"'''
    titleSet = re.findall(objre, data)
    for t in titleSet:
        mp[str(t)] = url

for item in mp:
    print(item, mp[item])