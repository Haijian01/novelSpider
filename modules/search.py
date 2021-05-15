import urllib3
from lxml import etree
from modules import noveldownload

def search_content(http, searchKey):
    searchUrl = 'http://www.shuquge.com/search.php'
    searchForm={'searchkey': searchKey}
    r = http.request('POST',searchUrl,fields=searchForm)
    content = r.data
    return content

def get_document_root(content):
    root = etree.HTML(content)
    return root

def get_search_url_list(root):
    searchUrlList = root.xpath('//div[@class="bookcase"]//h4[@class="bookname"]/a/@href')
    return searchUrlList
    
def get_search_name_list(root):
    searchNames = root.xpath('//div[@class="bookcase"]//h4[@class="bookname"]/a/text()')
    return searchNames

def get_search_result_group_list(root,homeUrl):
    searchUrlList = root.xpath('//div[@class="bookcase"]//h4[@class="bookname"]/a/@href')
    searchNames = root.xpath('//div[@class="bookcase"]//h4[@class="bookname"]/a/text()')
    searchResultGroup = []
    for index,url in enumerate(searchUrlList):
        searchResult = {}
        searchResult['index']=index
        searchResult['name']=searchNames[index]
        searchResult['url']=homeUrl+url.replace("/index.html", "/");
        searchResultGroup.append(searchResult)
    return searchResultGroup

def get_search_result_group_by_search_key(skey):
    homeUrl = 'http://www.shuquge.com'
    searchUrl = 'http://www.shuquge.com/search.php'
    http = urllib3.PoolManager()
    searchKey = skey
    content = search_content(http,searchKey)
    searchResultRoot = get_document_root(content)
    searchNames = get_search_name_list(searchResultRoot)
    searchUrlList = get_search_url_list(searchResultRoot)
    searchResultGroup = get_search_result_group_list(searchResultRoot,homeUrl)
    return searchResultGroup

def download_novels_by_search_key(skey):
    searchResultGroup = get_search_result_group_by_search_key(skey)
    print(searchResultGroup)
    for index,r in enumerate(searchResultGroup):
        url = r['url']
        print(url)
        noveldownload.get_novel_by_home_url(url)