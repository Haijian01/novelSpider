import urllib3
from lxml import etree
import os
from pathlib import Path

def get_url_content(http,url):
    r = http.request('GET',url)
    content = r.data
    return content

def get_document_root(content):
    root = etree.HTML(content)
    return root

def get_novel_name(root):
    novelName = root.xpath('//div[@class="book"]/div/h2/text()')
    return novelName[0]

def get_chapter_name(root):
    chapterName = root.xpath('//div[@class="book reader"]/div[@class="content"]/h1/text()')
    return chapterName[0]

def get_chapter_str_content(root):
    chapterName = get_chapter_name(root)
    viewContent = root.xpath('//div[@class="content"]/div[@id="content"]/text()')
    finalStrContent = chapterName+"\n"
    for view in viewContent:
        view = view.replace("\xa0", "");
        if view == '\r':
            continue
        finalStrContent = finalStrContent+view
    return finalStrContent

def get_url_list(root):
    urlList = root.xpath('//div[@class="listmain"]//dt[2]/following-sibling::dd/a/@href')
    return urlList

def get_chapter_name_list(root):
    chapterNameList = root.xpath('//div[@class="listmain"]//dt[2]/following-sibling::dd/a/text()')
    return chapterNameList

def process_chapters_into_file(http,novelName,homeUrl,urlList,chapterNameList):
    folderName = 'novels'
    create_novel_folder(folderName)
    nNamePath = folderName+'/'+novelName+".txt"
    if os.path.isfile(nNamePath):
        os.remove(nNamePath)
    f = open(nNamePath, "a+", encoding="utf8" )
    for index,u in enumerate(urlList):
        # print('downloading...'+chapterNameList[index])
        chapterDomContent = get_url_content(http,homeUrl+u)
        chapterDomRoot = get_document_root(chapterDomContent)
        chapterStrContent = get_chapter_str_content(chapterDomRoot)
        f.write(chapterStrContent+"\n")
        # print('finished '+chapterNameList[index])
    f.close()

def create_novel_folder(folder='novel'):
    # if os.path.isfile(folder):
    fpath = Path(folder)
    if fpath.is_dir() == False:
        os.mkdir(folder)


def get_novel_by_home_url(url):
    homeUrl = url
    cachedName = 'cached.txt'
    cache = ''
    if os.path.isfile(cachedName):
        f = open(cachedName, "r", encoding="utf8" )
        cache = f.read()
        f.close()
    if homeUrl in cache:
        print('url-{} already cached'.format(homeUrl))
        return
    http = urllib3.PoolManager()
    homeDomContent = get_url_content(http,homeUrl)
    homeDomRoot = get_document_root(homeDomContent)
    novelName = get_novel_name(homeDomRoot)
    urlList = get_url_list(homeDomRoot)
    chapterNameList = get_chapter_name_list(homeDomRoot)
    process_chapters_into_file(http,novelName,homeUrl,urlList,chapterNameList)
    f = open(cachedName, "a+", encoding="utf8" )
    f.write(novelName+' '+url+"\n")
    f.close()
