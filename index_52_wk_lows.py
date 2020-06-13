from NseStockAnalyser.utils import *
from pprint import pprint


def index_52_wk_lows():

    index = get_index()
    # slicing off 1st index of the data list since it contains index data
    nifty50_stocks_data_json = get_index_stock_data_json(index)['data'][1:]

    try:
        data_pts = int(input(f'Enter number of data points (Input Range : 1 - {len(nifty50_stocks_data_json)}): '))
        if not 1 <= data_pts <= len(nifty50_stocks_data_json):
            raise ValueError
    except ValueError:
        print('Please enter a valid input')
        return

    stocks_list = []
    for stocks in nifty50_stocks_data_json:
        try:
            code = stocks['meta']['symbol']
        except KeyError:
            code = stocks['symbol']

        cur_price = float(stocks['lastPrice'])
        yr_low = float(stocks['yearLow'])
        price_diff_from_low = round(cur_price - yr_low, 2)
        percent_above_low = round((price_diff_from_low / yr_low) * 100, 2)
        stocks_list.append({'code': code, 'cur_price': cur_price, 'yr_low': yr_low,
                            'price_diff_from_low': price_diff_from_low,
                            'percent_above_low': percent_above_low})

    stocks_list = sorted(stocks_list, key=lambda i: i['percent_above_low'])

    df = pd.DataFrame(stocks_list)
    df.columns = ['Stock Code', 'Current Price(INR)', '52 Week Low', 'Price Difference', '% Above Low']
    df.index = df.index + 1
    print('\n')
    print(df.head(data_pts))
    print('\n')