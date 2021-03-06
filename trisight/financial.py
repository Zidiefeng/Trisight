import requests
from trisight import token_check
from trisight import timeT as t
import datetime
from dateutil.relativedelta import *
import datetime as dt
import pandas as pd
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

token = token_check.get_token(token_check.token)
api_key = "5a5ff45c6674cc273285168d581aef6b"


def next_release_date(stock_code, n_months=3, token=token):
    '''Get next release date (string) within n months from today

    Use example:
        .. code-block:: python

            next_release_date("AAPL",n_months=1)

    :param stock_code: stock code, ex. "AAPL"
    :type stock_code: str

    :param n_months: how many months ahead to search release date (defualt=3)
    :type n_months: int

    :param token: token, optional, ex."btapdan48v6stqoinlu0"
    :type token: str

    :returns: string date (if exists), False (if not exists)
    :rtype: str
    '''
    now = dt.datetime.now()
    months_later = now+relativedelta(months=+n_months)
    str_today = now.strftime("%Y-%m-%d")
    str_m_after = months_later.strftime("%Y-%m-%d")
    df=quarterly_estimate_actual(stock_code, now, str_m_after, token=token)
    if df.shape[0]==0:
        print(f"No {stock_code} future release found within {n_months} months from today")
        result= False
    else:
        result= df.date.iloc[0]
    return result


def quarterly_estimate_actual(stock_code, from_date, to_date, api_key=api_key):
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
    # finnhub
    # req=f'https://finnhub.io/api/v1/calendar/earnings?from={from_date}&to={to_date}&symbol={stock_code}&token={token}'
    # req=requests.get(req).json()
    # df=pd.DataFrame(req['earningsCalendar'])

    # modeling: only company
    # req= f'https://financialmodelingprep.com/api/v3/historical/earning_calendar/{stock_code}?from={from_date}&to={to_date}&apikey={api_key}'
    # req=requests.get(req).json()
    # df=pd.DataFrame(req)
    # df.head()

    req=f"https://financialmodelingprep.com/api/v3/earning_calendar?from={from_date}&to={to_date}&apikey={api_key}"
    req=requests.get(req).json()
    df=pd.DataFrame(req)
    df = df[df.symbol==stock_code].reset_index(drop=True)

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
    reports = pd.concat([quarter_reports,annual_reports]).sort_values(by=['year', 'quarter','cik'], ascending=[False,False,True]).set_index(['filedDate'],drop=True)

    # drop duplicates due to different set of cik
    reports = reports.drop_duplicates(subset=['year','quarter'])
    return reports


def extract_last_file_date(stock_code, target_datetime, restrict_to_90d = True, token=token):
    '''Get the report file date of a company right before target date time within 90d/1y

    Use example:
        .. code-block:: python

            extract_last_file_date("AAL", "2020-09-20 00:00:00")
            extract_last_file_date("AAL", "2020-09-20 00:00:00", restrict_to_90d = False)

    :param stock_code: stock code, ex. "AAPL"
    :type stock_code: str

    :param target_datetime: target date time, "2019-10-24 00:00:00"
    :type target_datetime: str

    :param restrict_to_90d: default is True(only check previous 90d), False(check previous 1y)
    :type restrict_to_90d: bool

    :param token: token, optional, ex."btapdan48v6stqoinlu0"
    :type token: str

    :returns: file date right before 90d/1y **or** False (if not found)
    :rtype: str

    '''
    date_list= extract_reports(stock_code,token).index
    last_file_date= False
    restrict_days=93
    if not restrict_to_90d:
        restrict_days=365
    for i in date_list:
        target = t.str_to_dt(target_datetime)
        fileDate = t.str_to_dt(i)
        if (target - fileDate >= datetime.timedelta(0)) and (target -fileDate <= datetime.timedelta(restrict_days)):
            last_file_date=i
            break
    if last_file_date== False :
        print(f'No avaliable reports for {stock_code} within {restrict_days} days before {target_datetime}!')
    return last_file_date


def extract_recent_reports(stock_code,target_datetime,restrict_to_90d = True, token=token):

    '''Get the most recent report dict of a company <= target date time (within 90d/1y)

    Use example:
        .. code-block:: python

            extract_recent_reports("AAL", "2020-09-20 00:00:00")
            extract_recent_reports(stock_code="AAL",target_datetime="2020-09-26 00:00:00", restrict_to_90d=False)

    :param stock_code: stock code, ex. "AAPL"
    :type stock_code: str

    :param target_datetime: target date time, "2019-10-24 00:00:00"
    :type target_datetime: str

    :param restrict_to_90d: default is True(only check previous 90d), False(check previous 1y)
    :type restrict_to_90d: bool

    :param token: token, optional, ex."btapdan48v6stqoinlu0"
    :type token: str

    :returns: recent report dict (keys: ["balanceSheet","incomeStatement","cashFlow", ...], each can extract a dataframe)
    :rtype: dict

    '''

    reports = extract_reports(stock_code,token)
    file_date = extract_last_file_date(stock_code, target_datetime, restrict_to_90d=restrict_to_90d, token=token)
    if file_date==False:
        return False
    else:
        bs=pd.DataFrame(reports.loc[file_date]["report"]["bs"])
        ic=pd.DataFrame(reports.loc[file_date]["report"]["ic"])
        cf=pd.DataFrame(reports.loc[file_date]["report"]["cf"])
        if bs.shape[0] == 0:
            print(f"No balance sheet available for {stock_code} at {file_date}")
        if ic.shape[0] == 0:
            print(f"No income statement available for {stock_code} at {file_date}!")
        if cf.shape[0] == 0:
            print(f"No cash flow report available for {stock_code} at {file_date}!")
        reports_dict = {'symbol':reports.loc[file_date]['symbol'],
                        'year':reports.loc[file_date]['year'],
                        'quarter':reports.loc[file_date]['quarter'],
                        'form':reports.loc[file_date]['form'],
                        'startDate':reports.loc[file_date]['startDate'],
                        'endDate':reports.loc[file_date]['endDate'],
                        'fileDate':file_date,
                        "balanceSheet": bs,
                        "incomeStatement": ic,
                        "cashFlow": cf}
        return reports_dict
