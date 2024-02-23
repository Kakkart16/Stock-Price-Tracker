from django.shortcuts import render
import yahoo_fin.stock_info as si
# from yahoo_fin import stock_info
import yfinance as yf
import time
import queue
from threading import Thread
import json


def home(request):
    stock_picker = si.tickers_nifty50()
    # print(stock_picker)
    return render(request, 'home.html', {'stock_picker': stock_picker})

# def stockTracker(request):
#     selected_stocks = request.GET.getlist('stock')
#     data = {}
#     for stock in selected_stocks:
#         print(stock)
#         details = si.get_quote_table(stock)
#         data.update(details)

#     return render(request, 'stockTracker.html')



def stockTracker(request):
    selected_stocks = request.GET.getlist('stock')    
    dataX = {}
    # for stock in selected_stocks:
    #     quote = yf.Ticker(stock).info
    #     # print(quote)
    #     details = {
    #         'name': quote['shortName'],
    #         'price': quote["currentPrice"],
    #         'prev_close': quote["previousClose"], 
    #         'open': quote["open"],
    #         'market_cap': quote["marketCap"],
    #         'volume': quote["volume"],          
    #     }
    #     data.append(details)
    # print(data)
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

    # print(data)
    
    return render(request, 'stockTracker.html', {'data': data})
