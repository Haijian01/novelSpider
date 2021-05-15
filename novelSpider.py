import time
import queue
import threading
from modules import noveldownload 
from modules import search

def work(q):
    while True:
        if q.empty():
            return
        else:
            r = q.get()
            url = r['url']
            novelName = r['name']
            tid = r['index']
            print("threadId-{} novelName-{} , url-{} downloading...".format(tid,novelName,url))
            noveldownload.get_novel_by_home_url(url)
            print("threadId-{} novelName-{} , url-{} finished.".format(tid,novelName,url))

def main(searchResultGroup,condition,thread_num = 5):
    q = queue.Queue()
    for r in searchResultGroup:
        if condition['isSameName']:
            if r['name'] == condition['searchKey']:
                q.put(r)
        else:
            q.put(r)
    threads = []
    for i in range(thread_num):
        t = threading.Thread(target=work, args=(q,))
        threads.append(t)
    for i in range(thread_num):
        threads[i].start()
    for i in range(thread_num):
        threads[i].join()

if __name__ == "__main__":
    start = time.time()
    novelSource = 'shuquge'
    searchKey = '间客'

    search.initNovelSource(novelSource)
    noveldownload.initNovelSource(novelSource)

    condition = {}
    condition['isSameName'] = True
    condition['searchKey'] = searchKey

    searchResultGroup = search.get_search_result_group_by_search_key(searchKey,novelSource)
    print(searchResultGroup)
    main(searchResultGroup,condition)
    print('耗时：', time.time() - start)