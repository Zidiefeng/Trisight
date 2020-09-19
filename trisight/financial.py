import requests
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

def quarterly_estimate_actual(stock_code, from_date, to_date, token):
    '''Get estimate vs. actual EPS and revenue of each quarterly report,
    no info loss, no need to keep json

    Use example:
        quarterly_estimate_actual("AAPL", "2019-08-31","2020-09-11","btapdan48v6stqoinlu0")

    :param stock_code:
        stock code, ex. "AAPL"
    :type stock_code:
        str

    :param from_date:
        time string, ex."2020-09-11"
    :type from_date: str

    :param to_date:
        time string, ex."2020-09-11"
    :type to_date:
        str


    :returns:
        dataframe (row: report)
    :rtype:
        pd.DataFrame
    '''

    req=f'https://finnhub.io/api/v1/calendar/earnings?from={from_date}&to={to_date}&symbol={stock_code}&token={token}'
    req=requests.get(req).json()
    df=pd.DataFrame(req['earningsCalendar'])

    return df
