from celery import shared_task
import yahoo_fin.stock_info as si
import yfinance as yf
import time
import queue
from threading import Thread

@shared_task(bind = True)
def update_stock(self, selected_stocks):
    dataX = {}
    n_threads = len(selected_stocks)
    thread_list = []
    que = queue.Queue()
    for i in range(n_threads):
        quote = yf.Ticker(selected_stocks[i]).info
        # print(quote)
        details = {
            'name': quote['shortName'],
            'price': quote["currentPrice"],
            'prev_close': quote["previousClose"], 
            'open': quote["open"],
            'market_cap': quote["marketCap"],
            'volume': quote["volume"],  
            'change': quote['currentPrice'] - quote['previousClose']       
        }
        thread = Thread(target = lambda q, arg1: q.put({selected_stocks[i]: details}), args = (que, selected_stocks[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        dataX.update(result)
        
    # print(dataX)
    data = [value for value in dataX.values()]
    return 'done'    
