from django.shortcuts import render
import yahoo_fin.stock_info as si
# from yahoo_fin import stock_info
import yfinance as yf

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
    data = []
    for stock in selected_stocks:
        quote = yf.Ticker(stock).info
        # print(quote)
        details = {
            'name': quote['shortName'],
            'price': quote["currentPrice"],
            'prev_close': quote["previousClose"], 
            'open': quote["open"],
            'market_cap': quote["marketCap"],
            'volume': quote["volume"],          
        }
        data.append(details)
    # print(data)
    return render(request, 'stockTracker.html', {'data': data})
