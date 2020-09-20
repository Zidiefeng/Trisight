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


def extract_reports(stock_code,token=token):
    '''Get all finantial statements (balance sheet, income statement, cash flow) of a company

    Use example:
        .. code-block:: python

            extract_reports("UAL")

    :param stock_code: stock code, ex. "AAPL"
    :type stock_code: str

    :param token: token, optional, ex."btapdan48v6stqoinlu0"
    :type token: str

    :returns: dataframe (row: a set of quarterly financial report, in "report" json column))
    :rtype: pd.DataFrame

    '''

    # quarter reports (1,2,3)
    req=f'https://finnhub.io/api/v1/stock/financials-reported?symbol={stock_code}&freq=quarterly&token={token}'
    req=requests.get(req).json()['data']
    quarter_reports = pd.DataFrame(req)

    # annual reports (0)
    req=f'https://finnhub.io/api/v1/stock/financials-reported?symbol={stock_code}&freq=annual&token={token}'
    req=requests.get(req).json()['data']
    annual_reports = pd.DataFrame(req)

    # integrate reports, sort
    reports = pd.concat([quarter_reports,annual_reports]).sort_values(by=['year', 'quarter','cik'], ascending=[False,False,True]).reset_index()

    # drop duplicates due to different set of cik
    reports = reports.drop_duplicates(subset=['year','quarter'])
    return reports
