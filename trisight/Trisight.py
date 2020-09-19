# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 21:45:29 2020

@author: zgh72
"""

import finnhub
import pandas as pd
import pprint
import requests
import json
import smtplib, ssl
import numpy as np
#from datetime import datetime
import datetime
from datetime import timedelta
from dateutil.relativedelta import *
pd.set_option('display.max_columns', None)
finnhub_client = finnhub.Client(api_key="bt2sfov48v6sqcs91f30")

# from timestamp to date time
def stamp_to_dt(timestamp):
    dt = datetime.datetime.fromtimestamp(timestamp)
    #print("date time：", dt)
    return dt

# from string to date time
def str_to_dt(dt_str):
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    #print("date time：", dt)
    return dt

# from dt to timestamp
def dt_to_stamp(dt):
    timestamp = datetime.datetime.timestamp(dt)
    #print("date time：", dt)
    #print(timestamp)
    return timestamp

# from string to timestamp
def str_to_stamp(dt_str):
    timestamp = dt_to_stamp(str_to_dt(dt_str))
    #print(timestamp)
    return timestamp
#############################################################################################################################
def Earning_Calander(stock_code, from_date, to_date):
    #如果要锁定公司：https://finnhub.io/api/v1/calendar/earnings?from=2020-03-12&to=2020-03-15&symbol=ORBT&token=bt2sfov48v6sqcs91f30
    EC_string='https://finnhub.io/api/v1/calendar/earnings?from={}&to={}&symbol={}&token=btapdan48v6stqoinlu0'.format(from_date,to_date,stock_code)
    EC=requests.get(EC_string)
    print(EC.json()['earningsCalendar'])
    
    return pd.DataFrame(EC.json()['earningsCalendar']).drop(["quarter","year"],axis=1)
Earning_Calander_list=Earning_Calander("AAPL", "2019-08-31","2020-09-11")
#计算每个quarer之间eps Estimate的变化率，注意，由于最新一期的estimate往往在接近财报日才会出现，因此往往第一个值都是NaN；
#计算思路是（上一个earning date的EPS estimate-这次财报日的EPS earning estimate）/这次财报日的EPS earning estimate
Earning_Calander_list['epsEstimate'].pct_change()
#每个quarter之间revenue Estimate的变化率
Earning_Calander_list['revenueEstimate'].pct_change()

def EPS_latest_estimate(stock_code, to_date):
    to_date_future=str_to_dt(to_date)+relativedelta(months=+1)
    from_date=str_to_dt(to_date)+relativedelta(months=-3)
    #如果要锁定公司：https://finnhub.io/api/v1/calendar/earnings?from=2020-03-12&to=2020-03-15&symbol=ORBT&token=bt2sfov48v6sqcs91f30
    EC_string='https://finnhub.io/api/v1/calendar/earnings?from={}&to={}&symbol={}&token=btapdan48v6stqoinlu0'.format(from_date,to_date_future,stock_code)
    EC=requests.get(EC_string)
    print(EC.json()['earningsCalendar'])
    return pd.DataFrame(EC.json()['earningsCalendar'])['epsEstimate'][0]

def EPS_latest_actual(stock_code, to_date):
    to_date_future=str_to_dt(to_date)+relativedelta(months=+1)
    from_date=str_to_dt(to_date)+relativedelta(months=-3)
    #如果要锁定公司：https://finnhub.io/api/v1/calendar/earnings?from=2020-03-12&to=2020-03-15&symbol=ORBT&token=bt2sfov48v6sqcs91f30
    EC_string='https://finnhub.io/api/v1/calendar/earnings?from={}&to={}&symbol={}&token=btapdan48v6stqoinlu0'.format(from_date,to_date_future,stock_code)
    EC=requests.get(EC_string)
    print(EC.json()['earningsCalendar'])
    
    return pd.DataFrame(EC.json()['earningsCalendar'])['epsActual'][1]
#############################################################################################################################
def Latest_Reported_Financial_bs(stock_code):
    RF_string='https://finnhub.io/api/v1/stock/financials-reported?symbol={}&freq=quarterly&token=btapdan48v6stqoinlu0'.format(stock_code)
    RF=requests.get(RF_string)
    return pd.DataFrame(RF.json()['data'][0]['report']['bs'])
def Latest_Reported_Financial_cf(stock_code):
    RF_string='https://finnhub.io/api/v1/stock/financials-reported?symbol={}&freq=quarterly&token=btapdan48v6stqoinlu0'.format(stock_code)
    RF=requests.get(RF_string)
    return pd.DataFrame(RF.json()['data'][0]['report']['cf'])
def Latest_Reported_Financial_ic(stock_code):
    RF_string='https://finnhub.io/api/v1/stock/financials-reported?symbol={}&freq=quarterly&token=btapdan48v6stqoinlu0'.format(stock_code)
    RF=requests.get(RF_string)
    return pd.DataFrame(RF.json()['data'][0]['report']['ic'])

def RF_calender(stock_code):
    RF_string='https://finnhub.io/api/v1/stock/financials-reported?symbol={}&freq=quarterly&token=btapdan48v6stqoinlu0'.format(stock_code)
    RF=requests.get(RF_string)
    RF_calender={}
    for i in range(len(RF.json()['data'])):
        RF_calender[RF.json()['data'][i]['filedDate']]=RF.json()['data'][i]['report']
    return RF_calender

def search_RF(stock_code, target_date):
    date_list=list(RF_calender(stock_code).keys())
    target_RF_date=''
    for i in date_list:
        if datetime.timedelta(0)<str_to_dt(target_date)-str_to_dt(i) and str_to_dt(target_date)-str_to_dt(i) < datetime.timedelta(93): 
            target_RF_date=i
            break
        else:
            target_RF_date='Cannot find the avaliable reported financial based on this target date!'
    return target_RF_date

def RF_date_info(stock_code):
    RF_string='https://finnhub.io/api/v1/stock/financials-reported?symbol={}&freq=quarterly&token=btapdan48v6stqoinlu0'.format(stock_code)
    RF=requests.get(RF_string)
    RF_date_info={}
    for i in range(len(RF.json()['data'])):        
        RF_date_info[RF.json()['data'][i]['filedDate']]={'year':RF.json()['data'][i]['year'],
                                                             'quarter':RF.json()['data'][i]['quarter'],
                                                             'form':RF.json()['data'][i]['form'],
                                                             'startDate':RF.json()['data'][i]['startDate'],
                                                             'endDate':RF.json()['data'][i]['endDate']}
    return RF_date_info
                                                            
#search_RF_bs('AAPL','2020-04-29 00:00:00')结果有两个部分：
#[0]表示基于target date检索到的报表日期对应的日期细节
#[1]表示基于target date检索道德报表日期对应的bs报告
    
def search_RF_bs(stock_code, target_date):
    RF_info=RF_date_info(stock_code)[search_RF(stock_code, target_date)]
    RF_target_bs=pd.DataFrame(RF_calender(stock_code)[search_RF(stock_code, target_date)]['bs'])
    RF_target_bs=RF_target_bs.set_index('label')
    return RF_info,RF_target_bs
def ratio(value1,value2):
    ratio=value1/value2
    return round(ratio,2)
total_current_asset=search_RF_bs('AAPL','2020-07-29 00:00:00')[1].loc['Total current assets']['value']
total_current_liability=search_RF_bs('AAPL','2020-07-29 00:00:00')[1].loc['Total current liabilities']['value']
total_current_ratio=ratio(total_current_asset,total_current_liability)
def financial_ratio_list(stock_code,target_date):
    #Total current ratio
    RF_target_bs=search_RF_bs('AAPL','2020-07-29 00:00:00')[1]
    total_current_asset=RF_target_bs.loc['Total current assets']['value']
    total_current_liability=RF_target_bs.loc['Total current liabilities']['value']
    total_current_ratio=ratio(total_current_asset,total_current_liability)
    #Quick Ratio
    quick_asset=total_current_asset-RF_target_bs.loc['Inventories']['value']-RF_target_bs.loc['Accounts receivable, net']['value']-RF_target_bs.loc['Vendor non-trade receivables']['value']
    quick_ratio=ratio(quick_asset,total_current_liability)
    #保守速动比率，现金比率，现金流量比率都没有计算
    
    #Asset Liability Ratio
    total_liability=RF_target_bs.loc['Total liabilities']['value']
    total_asset=RF_target_bs.loc['Total assets']['value']
    asset_liability_ratio=ratio(total_liability,total_asset)
    
    return {'total_current_ratio':total_current_ratio, 
            'quick_ratio':quick_ratio,
            'asset_liability_ratio':asset_liability_ratio}