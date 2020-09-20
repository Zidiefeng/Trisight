import requests
from trisight import token_check
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

token = token_check.get_token(token_check.token)

def quarterly_estimate_actual(stock_code, from_date, to_date, token=token):
    '''Get estimate vs. actual EPS and revenue of each quarterly report (no info loss)

    Use example:
        .. code-block:: python

            quarterly_estimate_actual("AAPL", "2019-08-31","2020-09-11","btapdan48v6stqoinlu0")
            quarterly_estimate_actual("AAPL", "2019-08-31","2020-09-11")

    :param stock_code: stock code, ex. "AAPL"
    :type stock_code: str

    :param from_date: time string, ex."2020-09-11"
    :type from_date: str

    :param to_date: time string, ex."2020-09-11"
    :type to_date:str

    :param token: token, optional, ex."btapdan48v6stqoinlu0"
    :type token: str


    :returns: dataframe (row: report)
    :rtype: pd.DataFrame
    '''

    req=f'https://finnhub.io/api/v1/calendar/earnings?from={from_date}&to={to_date}&symbol={stock_code}&token={token}'
    req=requests.get(req).json()
    df=pd.DataFrame(req['earningsCalendar'])

    return df
