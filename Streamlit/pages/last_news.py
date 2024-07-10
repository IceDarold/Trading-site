import streamlit as st
from Utilities.Parsers import lenta_parser
from Utilities.Parsers import ria_parser
from datetime import datetime
import pandas as pd

st.title("Парсинг новостей")
st.markdown("Здесь можно посмотреть новости")
st.header("Ria новости")
with open("Data/News/ria.csv", "r", encoding='utf-8') as f:
    f.readline()
    df = f.readline()
article_l = []
comma_index = df.find(',')
ria = df[:comma_index]
with open("Data/News/lenta.csv", "r", encoding='utf-8') as f:
    f.readline()
    df = f.readline()
article_l = []
comma_index = df.find(',')
lenta = df[:comma_index]
# slash_index = df.find('https://')
# title = df[comma_index + 1:slash_index-1]
# url = df[slash_index:]
# article_l.append([date, title, url])
# df = pd.DataFrame(article_l, columns=["datetime", "Title", "Url"])
print(lenta, ria)
lenta_parser.parse(datetime.strptime(ria, '%Y-%m-%d %H:%M:%S'), datetime.now(), "Data/News/ria.csv")
lenta_parser.parse(datetime.strptime(lenta, '%Y-%m-%d %H:%M:%S'), datetime.now(), "Data/News/lenta.csv")
# st.dataframe(df)
st.header("Lenta.ru")