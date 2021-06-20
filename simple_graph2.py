import FinanceDataReader as fdr
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)


# 한글, 영어 구분; 한글 -> 'k', 영어 ->'e'
def isEnglishOrKorean(input_s):
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count += 1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count += 1
    return "k" if k_count > 1 else "e"


# 한국기업은 기업명, 미국기업은 티커 입력 -> symbol, name
def stock_code(val):
    if isEnglishOrKorean(val) == 'e':
        df_nsq = fdr.StockListing('LASDAQ')
        df_nyse = fdr.StockListing('NYSE')
        df_us = pd.concat([df_nsq, df_nyse])
        df_name = df_us[df_us['Symbol'] == val]
        symbol = df_name.iloc[0, 0]
        name = df_name.iloc[0, 1]
    else:
        df_krx = fdr.StockListing('KRX')
        df_name = df_krx[df_krx['NAME'] == val]
        symbol = df_name.iloc[0, 0]
        name = df_name.iloc[0, 2]

    return symbol, name


# Price chart 그리기
def price_chart(company, year):
    title = stock_code(company)[1] + '(' + stock_code(company)[0] + ')'
    titles = dict(text=title, x=0.5, y=0.85)

    df = fdr.DataReader(stock_code(company)[0], year)

    fig = make_subplots(specs=[[{'secondary_y': True}]])
    x = df.index.tolist()
    y = df['Close']
    fig.add_trace(go.Scatter(mode='lines', name='주가', x=x, y=y))
    annotations = []
    annotations.append(dict(xref='paper', yref='paper', x=0.5, y=-0.1, xanchor='center', yanchor='top',
                            text='주가 그래프',
                            font=dict(family='Arial', size=12, color='rgb(150,150,150)'),
                            showarrow=False))

    annotations.append(dict(xref='paper', x=0.95, y=y.tail(1)[0],
                            xanchor='left', yanchor='middle',
                            text=str(x[-1:])[12:22] + ' : ' + f'{y.tail(1)[0]:,.0f}',
                            font=dict(family='Arial', size=12),
                            showarrow=False))

    fig.upodate_layout(title=titles, titlefont_size=15, annotations=annotations)
    fig.show()


print(stock_code('삼성전자'))
#price_chart('삼성전자', 2020)
