import urllib3
from lxml import etree
from modules import noveldownload
from settings import settings

# searchUrl = 'http://www.shuquge.com/search.php'
# searchFormKey = 'searchkey'
# searchResultNovelUrlListXpath = '//div[@class="bookcase"]//h4[@class="bookname"]/a/@href'
# searchResultNovelNameListXpath = '//div[@class="bookcase"]//h4[@class="bookname"]/a/text()'
# homeUrl = 'http://www.shuquge.com'
searchSetting = {}
# searchUrl = ''
# searchFormKey = ''
# searchResultNovelUrlListXpath = ''
# searchResultNovelNameListXpath = ''
# homeUrl = ''

def initNovelSource(source='shuquge'):
    global searchSetting
    novelSource = source
    searchSetting = settings.settings[source]

# def initNovelSource(source='shuquge'):
#     global novelSource
#     global searchUrl
#     global searchFormKey,searchResultNovelUrlListXpath
#     global searchResultNovelNameListXpath,homeUrl
#     novelSource = source
#     ns = settings.settings
#     searchUrl = ns[novelSource]['searchUrl']
#     searchFormKey = ns[novelSource]['searchFormKey']
#     searchResultNovelUrlListXpath = ns[novelSource]['searchResultNovelUrlListXpath']
#     searchResultNovelNameListXpath = ns[novelSource]['searchResultNovelNameListXpath']
#     homeUrl = ns[novelSource]['homeUrl']

def search_content(http, searchKey):
    searchUrl = searchSetting['searchUrl']
    searchFormKey = searchSetting['searchFormKey']
    searchForm={ searchFormKey : searchKey}
    r = http.request('POST',searchUrl,fields=searchForm)
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
        print(url)
        noveldownload.get_novel_by_home_url(url)