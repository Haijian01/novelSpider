import search
import time
import queue
import threading
import noveldownload

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

def main(searchResultGroup,thread_num = 5):
    q = queue.Queue()
    for r in searchResultGroup:
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
    searchKey = '大秦帝国之纵横天下'
    searchResultGroup = search.get_search_result_group_by_search_key(searchKey)
    print(searchResultGroup)
    main(searchResultGroup)
    print('耗时：', time.time() - start)