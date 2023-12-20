from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
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

peri1 = st.sidebar.number_input('단기 일수', value = 50, step = 10)
peri2 = st.sidebar.number_input('장기 일수', value = 500, step = 50)

if peri1>0 and peri2 > 0 :
    db = get_table (peri1, peri2)
    day1 = (datetime.today()-timedelta(peri2)).strftime('%Y%m%d') # 시작일
    day2 = datetime.today().strftime('%Y%m%d')                    # 오늘
    db1 = db.loc[ (db.volume_change>1.5) & (db.등락률2<-30) & (db.등락률1<0) ]

    hei =2
    fig, axs = plt.subplots(len(db1), 1, figsize=(7,hei*len(db1)))

    for i,tk in enumerate(db1.index[:]):
        df = stock.get_market_ohlcv_by_date(day1, day2, tk)
        axs[i].plot( np.arange(len(df)), df.종가, color= 'k')
        axs[i].plot( np.arange(len(df)), df.종가.rolling(window=5).mean(), color= 'r')
        axs[i].set_xticklabels([])
        ax2 = axs[i].twinx()
        ax2.bar(np.arange(len(df)),df.거래량, color= 'k', alpha = 0.3)
        ax2.bar(np.arange(len(df)),df.거래량.rolling(window=5).mean(), color= 'r', alpha = 0.3)
        ax2.set_xticklabels([])
        axs[i].set_title(db1.loc[tk].종목명1)
        
        time.sleep(2)

    fig.set_tight_layout(1)

    st.text('후보 종목 개수: '+ str( len(db1)))

    st.pyplot(fig)