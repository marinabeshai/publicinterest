# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
from datetime import datetime,timedelta
from dateutil.parser import parse
import requests
import statistics
import utils.constants as constants 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def add_to_date(date, number_of_weeks):
    date = datetime.strptime(date, constants.DATE_FORMAT)
    date += timedelta(days = (number_of_weeks*7))
    
    if date.isoweekday() == 6:
        date = date + timedelta(days = 2)
    elif date.isoweekday() == 7:
        date = date + timedelta(days = 1)
        
    return datetime.strptime(str(date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT)
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Bought it for $20, Sold it for $40.
def share_diff(ticker, tdate_sale, tdate_purch):
    sale_price = get_stock_price(ticker, tdate_sale)
    purch_price = get_stock_price(ticker, tdate_purch)
    if purch_price and sale_price:
        return  round(sale_price,2) , round(purch_price,2), round((sale_price - purch_price)/purch_price, 4)
    return None, None, None 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_unix_timestamp(date):
    date = datetime.strptime(date, constants.DATE_FORMAT) - timedelta(days = 1)
    dt = datetime( date.year, date.month, date.day, 23, 59, 59)
    return int( dt.timestamp() )
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_stock_price(ticker, date, tries=0):
    try: 
        original_date  = datetime.strptime(date, constants.DATE_FORMAT)
 
        if ticker in constants.SOME_WRONG_TICKERS:
            ticker = constants.SOME_WRONG_TICKERS[ticker]
            
        period1 = get_unix_timestamp(date)
        date = datetime.strptime(date, constants.DATE_FORMAT)
        desired_date = datetime.strptime(str(date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT)
        
        # Friday
        if date.isoweekday() == 5:
            # Monday
            date = date + timedelta(days = 3)
            
        # Saturday
        elif date.isoweekday() == 6:
            date = date - timedelta(days = 1)
            period1 = get_unix_timestamp(datetime.strptime(str(date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT))

            # Monday
            date = date + timedelta(days = 2)

        # Sunday
        elif date.isoweekday() == 7:
            date = date - timedelta(days = 2)
            period1 = get_unix_timestamp(datetime.strptime(str(date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT))
            date = date + timedelta(days = 1)
            
        else:
            date = date + timedelta(days = 1)

            
        period2 = get_unix_timestamp(datetime.strptime(str(date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT))

        url = 'https://finance.yahoo.com/quote/{ticker}/history?period1={period1}&period2={period2}&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'.format(ticker=ticker, period1=period1, period2=period2)

        
        # print(url)
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15'

        headers = {'User-Agent': agent}

        response = requests.get(url, headers=headers)
        
        find = '<th class="Fw(400) Py(6px)"><span>Volume</span></th></tr></thead><tbody><tr class="BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)"><td class="Py(10px) Ta(start) Pend(10px)"><span>'
        
        if find in response.text:
            res = response.text[ response.text.find(find) + len(find) : ] 
        elif tries != 3:
            original_date += timedelta(days = 1)
            return get_stock_price(ticker, datetime.strptime(str(original_date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT), tries=tries+1)
        else:
            return None 
        
        find = 'Close price adjusted for splits.'
        if find in res:
            res = res[ : res.find(find)]
        elif tries != 3:
            original_date += timedelta(days = 1)
            return get_stock_price(ticker, datetime.strptime(str(original_date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT), tries=tries+1)
        else:
            return None 
        
        date_received = open = high = low = close = adj_close = volume =  0 


        find = '</span>'
        date_received = res[ : res.find(find)]
        date_received = datetime.strptime(str(parse(date_received).date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT)
        assert date_received == desired_date       
        res = res [res.find(find) + len(find) : ]
        
        find = '</td><td class="Py(10px) Pstart(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        open = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]
        
        find = '</td><td class="Py(10px) Pstart(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        high = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]
        
        find = '</td><td class="Py(10px) Pstart(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        low = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]

        find = '</td><td class="Py(10px) Pstart(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        close = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]

        find = '(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        adj_close = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]

        find = '</td><td class="Py(10px) Pstart(10px)"><span>'
        res = res [res.find(find) + len(find) : ] 
        find = '</span>'
        volume = float(res [ : res.find(find)].replace(",", ''))
        res = res [res.find(find) + len(find) : ]

        return statistics.mean([high, low]) 
    
    except Exception as e:
        # print(e)
        if tries != 3:
            original_date += timedelta(days = 1)
            return get_stock_price(ticker, datetime.strptime(str(original_date.date()), "%Y-%m-%d").strftime(constants.DATE_FORMAT), tries=tries+1)
        return None
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   
def get_instances(pm):
     # { (name, ticker) : { tdate_sale : [(diff, tdate_purch), (diff, tdate_purch), ....] } , .... }
    instances = {}

    for (name, ticker, tdate_sale) in pm.keys():
        l =  pm[(name, ticker, tdate_sale)]
        if (name, ticker) not in instances:
            instances[(name, ticker)] = {tdate_sale : l}    
        else:
            instances[(name, ticker)][tdate_sale] = l 

    return instances 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def stableMarriage(instance_value):
    srted = {}
    for k,v in instance_value.items():
        v = sorted(v, key=lambda a:a[0], reverse=True)
        srted[k] = v
    instance_value = srted
    
    
    x = list(instance_value.keys())
    y = list(instance_value.values())
    y = [val for l in y for val in l]

    availablePurchases = {}
    for _,i in y:
        availablePurchases[i] = -1 
    
    unmatchedSaleDates = len(x)

    availableSaleDates = {}
    for saleDate in x: 
        availableSaleDates[saleDate] = True 

    pickedSaleDate = None 
    
    saleIndex = 0 
    maxSaleIndex = len(instance_value.keys())

    while saleIndex < maxSaleIndex:
        pickedSaleDate = list(availableSaleDates)[saleIndex]
        purchaseIndex = 0 
        
        while purchaseIndex < len(instance_value[pickedSaleDate]) and availableSaleDates[pickedSaleDate]:

            local_prefs = instance_value[pickedSaleDate]
            x_diff, purch_date =  local_prefs[purchaseIndex]
            
            
            if availablePurchases[purch_date] == -1:
                availablePurchases[purch_date] = (x_diff, pickedSaleDate)
                availableSaleDates[pickedSaleDate] = False 
                unmatchedSaleDates -= 1 
                
            else:
                oldSaleMatch = availablePurchases[purch_date]
                x, y = oldSaleMatch
                aList = instance_value[y]

                for (y_diff, purchDate) in aList:
                    if purch_date == purchDate and y_diff < x_diff:
                        availablePurchases[purch_date] = (x_diff, pickedSaleDate)
                        availableSaleDates[y] = True 
                        availableSaleDates[pickedSaleDate] = False
                        break 
                    else:
                        break 
            
            purchaseIndex += 1 
        saleIndex += 1 
            
    return availablePurchases
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------