from django.shortcuts import render
import yahoo_fin.stock_info as si
from django.http.response import HttpResponse

# from yahoo_fin import stock_info
import yfinance as yf
import queue
from threading import Thread
from asgiref.sync import sync_to_async



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


@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True
    
async def stockTracker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
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
    return render(request, 'stockTracker.html', {'data': dataX, 'room_name': "track"})
