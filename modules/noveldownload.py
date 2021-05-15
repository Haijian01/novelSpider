import urllib3
from lxml import etree
import os
from pathlib import Path
from settings import settings
import shutil
import queue
import threading
import time

downloadSetting = {}

def initNovelSource(source='shuquge'):
    global downloadSetting
    downloadSetting = settings.settings[source]

def get_url_content(http,url):
    r = http.request('GET',url)
    content = r.data
    return content

def get_document_root(content):
    root = etree.HTML(content)
    return root

def get_novel_name(root):
    novelNameXpath = downloadSetting['novelNameXpath']
    novelName = root.xpath(novelNameXpath)
    return novelName[0]

def get_chapter_name(root):
    chapterNameXpath = downloadSetting['chapterNameXpath']
    chapterName = root.xpath(chapterNameXpath)
    return chapterName[0]

def get_chapter_str_content(root):
    chapterName = get_chapter_name(root)
    viewContentXpath = downloadSetting['viewContentXpath']
    removeSpecialSymbolsInViewContent = downloadSetting['removeSpecialSymbolsInViewContent']
    viewContent = root.xpath(viewContentXpath)
    finalStrContent = chapterName+"\n"
    for view in viewContent:
        view = view.replace(removeSpecialSymbolsInViewContent, "");
        if view == '\r':
            continue
        finalStrContent = finalStrContent+view
    return finalStrContent

def get_url_list(root):
    chapterUrlListXpath = downloadSetting['chapterUrlListXpath']
    urlList = root.xpath(chapterUrlListXpath)
    return urlList

def get_chapter_name_list(root):
    chapterNameListXpath = downloadSetting['chapterNameListXpath']
    chapterNameList = root.xpath(chapterNameListXpath)
    return chapterNameList

def create_html_tmp_folders():
    millis = int(round(time.time() * 1000))
    tempHtmlFolderName = 'tmpHtml' + str(millis)
    create_folder(tempHtmlFolderName)
    return tempHtmlFolderName

def download_chapter_task(q):
    while True:
        if q.empty():
            return
        else:
            args = q.get()
            http = args['http']
            homeUrl = args['homeUrl']
            url = args['url']
            index = args['index']
            folderName = args['folderName']
            chapterDomContent = get_url_content(http,homeUrl+url)
            nNamePath = folderName+'/'+str(index)+".html"
            if os.path.isfile(nNamePath):
                os.remove(nNamePath)
            f = open(nNamePath, "a+", encoding="utf8" )
            f.write(chapterDomContent.decode('utf8'))
            f.close()

def download_all_html_chapters_by_thread(http,homeUrl,urlList,thread_num = 5):
    tempHtmlFolderName = create_html_tmp_folders()
    q = queue.Queue()
    for index,u in enumerate(urlList):
        args = {}
        args['http'] = http
        args['homeUrl'] = homeUrl
        args['url'] = u
        args['index'] = index
        args['folderName'] = tempHtmlFolderName
        q.put(args)
    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=download_chapter_task, args=(q,))
        threads.append(t)
    for i in range(thread_num):
        threads[i].start()
    for i in range(thread_num):
        threads[i].join()
    return tempHtmlFolderName

def delete_folder(nNamePath):
    shutil.rmtree(nNamePath)

def get_file_content(fileName):
    content = ''
    if os.path.isfile(fileName):
        f = open(fileName, "r", encoding="utf8" )
        content = f.read()
        f.close()
    return content

def process_chapters_into_file(http,novelName,homeUrl,urlList,chapterNameList):
    folderName = 'novels'
    create_novel_folder(folderName)

    tempHtmlFolderName = download_all_html_chapters_by_thread(http,homeUrl,urlList)

    nNamePath = folderName+'/'+novelName+".txt"
    if os.path.isfile(nNamePath):
        os.remove(nNamePath)
    f = open(nNamePath, "a+", encoding="utf8" )
    for index,u in enumerate(urlList):
        filepath = tempHtmlFolderName + '/' + str(index) + '.html'
        chapterDomContent = get_file_content(filepath)
        chapterDomRoot = get_document_root(chapterDomContent)
        chapterStrContent = get_chapter_str_content(chapterDomRoot)
        f.write(chapterStrContent+"\n")
    f.close()
    delete_folder(tempHtmlFolderName)

def create_folder(folder='temp'):
    fpath = Path(folder)
    if fpath.is_dir() == False:
        os.mkdir(folder)

def create_novel_folder(folder='novel'):
    create_folder(folder)

def get_novel_by_home_url(url):
    homeUrl = url
    cachedName = 'cached.txt'
    cache = get_file_content(cachedName)
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
