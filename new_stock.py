
# from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
# import pykrx
# import matplotlib as plt
import time


def get_db(peri) :
    day1 = (datetime.today()-timedelta(peri)).strftime('%Y%m%d') # 시작일
    day2 = datetime.today().strftime('%Y%m%d')                  # 오늘
    df = stock.get_market_price_change_by_ticker(day1, day2)    # DB받음
    days = len(stock.get_market_ohlcv_by_date(day1, day2, "005930"))  #며칠간인가
    df['거래량'] = round(df['거래량']/days/1000,0)  #거래량은 일평균이 필요함
    return df[['종목명','등락률', '거래량']]

def get_table(peri1, peri2):
    db1 = get_db(peri1) #단기
    db2 = get_db(peri2) #장기
    db = pd.concat([db1,db2], axis=1)
    db.dropna(inplace = True)
    db. columns = ['종목명1', '등락률1', '거래량1', '종목명2', '등락률2', '거래량2']
    db['volume_change'] = np.round(db['거래량1']/db['거래량2'],2)
    return db

# peri1, peri2 = 30, 180

peri1 = st.sidebar.number_input('단기 일수')
peri2 = st.sidebar.number_input('장기 일수')
