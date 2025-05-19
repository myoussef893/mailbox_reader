import streamlit as st 
import pandas as pd 
from app import refunds_fetcher,sales_fetcher


st.set_page_config(layout='wide')
st.button('Update Sales:',on_click=sales_fetcher)
st.button('Update Refunds:',on_click = refunds_fetcher)

df = pd.read_sql('amazon_orders',con='sqlite:///app_base.db').dropna()
df['price'] = pd.to_numeric(df['price'])
gp = df.groupby(['item_title','sku_id'])['price'].sum().sort_values(ascending=False)
st.write(gp)
st.line_chart(data=df,x='order_date',y='price')
st.write(df.columns)

