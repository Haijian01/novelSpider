import urllib3
from lxml import etree
from modules import noveldownload
from settings import settings

searchSetting = {}

def initNovelSource(source='shuquge'):
    global searchSetting
    novelSource = source
    searchSetting = settings.settings[source]

def search_content(http, searchKey):
    searchUrl = searchSetting['searchUrl']
    searchFormKey = searchSetting['searchFormKey']
    searchForm={ searchFormKey : searchKey ,'searchtype': 'all'}
    r = http.request('POST',searchUrl,headers={'User-agent':'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36','Cookie':'Hm_lvt_359dc43321627151a4b3963ea8b7a00c=1621068443; Hm_lpvt_359dc43321627151a4b3963ea8b7a00c=1621068450'},fields=searchForm)
    content = r.data
    return content

def get_document_root(content):
    root = etree.HTML(content)
    return root

def get_search_url_list(root):
    searchResultNovelUrlListXpath = searchSetting['searchResultNovelUrlListXpath']
    searchUrlList = root.xpath(searchResultNovelUrlListXpath)
    return searchUrlList
    
def get_search_name_list(root):
    searchResultNovelNameListXpath = searchSetting['searchResultNovelNameListXpath']
    searchNames = root.xpath(searchResultNovelNameListXpath)
    return searchNames

def get_search_result_group_list(root,homeUrl,novelSource):
    searchResultNovelNameListXpath = searchSetting['searchResultNovelNameListXpath']
    searchResultNovelUrlListXpath = searchSetting['searchResultNovelUrlListXpath']

    searchUrlList = root.xpath(searchResultNovelUrlListXpath)
    searchNames = root.xpath(searchResultNovelNameListXpath)
    searchResultGroup = []
    for index,url in enumerate(searchUrlList):
        searchResult = {}
        searchResult['index']=index
        searchResult['name']=searchNames[index]
        searchResult['url']=homeUrl+url.replace("/index.html", "/");
        searchResult['novelSource']=novelSource
        searchResultGroup.append(searchResult)
    return searchResultGroup

def get_search_result_group_by_search_key(skey,novelSource):
    homeUrl = searchSetting['homeUrl']
    http = urllib3.PoolManager()
    searchKey = skey
    content = search_content(http,searchKey)
    searchResultRoot = get_document_root(content)
    searchNames = get_search_name_list(searchResultRoot)
    searchUrlList = get_search_url_list(searchResultRoot)
    searchResultGroup = get_search_result_group_list(searchResultRoot,homeUrl,novelSource)
    return searchResultGroup

def download_novels_by_search_key(skey):
    searchResultGroup = get_search_result_group_by_search_key(skey)
    print(searchResultGroup)
    for index,r in enumerate(searchResultGroup):
        url = r['url']
        noveldownload.get_novel_by_home_url(url)