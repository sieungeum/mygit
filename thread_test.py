# from bs4 import BeautifulSoup
# import grequests
# import requests
# import time
#
# start_time = time.time()
#
# links = [
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=1",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=2",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=3",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=4",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=5",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=6",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=7",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=8",
#
# "https://www.croma.com/phones-wearables/mobile-phones/c/10?q=%3Arelevance%3AskuStockFlag%3Atrue&page=9"
#
# ]
#
#
# for link in links:
#
#     req = requests.get(link)
#
#     soup = BeautifulSoup(req.text, 'lxml')
#
#     lists = soup.find_all('a', attrs={'class':"product__list--name"})
#
#     #print(lists[0].text)
#
#     prices = soup.find_all('span', attrs={'class':"pdpPriceMrp"})
#
#     #print(prices[0].text)
#
#     discount = soup.find_all("div", attrs={"class":"listingDiscnt"})
#
#     #print(discount[0].text)
#
# print("--- %s seconds ---" % (time.time() - start_time))
#
# # 비동기식 웹스크래핑
# reqs = (grequests.get(link) for link in links)
#
# resp = grequests.imap(reqs, grequests.Pool(10))
#
# for r in resp:
#
#     soup = BeautifulSoup(r.text, 'lxml')
#
#     results = soup.find_all('a', attrs={"class":'product__list-name'})
#
#     #print(results[0].text)
#
#     prices = soup.find_all('span', attrs={'class':"pdpPriceMrp"})
#
#     #print(prices[0].text)
#
#     discount = soup.find_all("div", attrs={"class":"listingDiscnt"})
#
#     #print(discount[0].text)
#
# print("--- %s seconds ---" % (time.time() - start_time))

# import threading
# import time
#
# def func0(list_var):
#     for x in list_var:
#         print(x)
#         time.sleep(0.5)
#
# def func1(list_var):
#     for x in list_var:
#         print(x)
#         time.sleep(1)
#
# if __name__ == "__main__":
#     # t2 = threading.Thread(target=func1, args= (["a", "b", "c"],))
#
#     a = [[1, 2, 3], [3, 4, 5], [6, 7, 8]]
#     for i in a:
#         t1 = threading.Thread(target=func0, args=(i,))
#         t1.start()
#         print(i)
#
#
#     print("Dddsfaf")
#     t1.join()
#     # func0([1,2,3])
#     # func1(["A","b","c"])

import threading
import queue

q = queue.Queue()
q1 = queue.Queue()

def f(v, queue, idx):
    b = {}
    """
    :param v: {"input": 특정 값, "output": None}
    :param queue: 계산 결과를 저장할 queue
    """

    for i in range(5):
        v["output"] = i + v["input"]
        b[i] = v

    queue.put(b)
    idx.put(len(b))


variables = [{"input": 1}, {"input": 5}, {"input": 3}, {"input": 2}, {"input": 9}]
threads = []

for var in variables:
    t = threading.Thread(target=f, args=(var, q, q1, ))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

count = 0
abc = {}
n = 0

for a, b in zip(q.queue, q1.queue):
    for i in a.values():
        abc[count] = i
        count += 1

print(count)
print(abc)


