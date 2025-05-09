import streamlit as st 
import pandas as pd 



df = pd.read_sql('amazon_orders',con='sqlite:///app_base.db').dropna()
df['price'] = pd.to_numeric(df['price'])
gp = df.groupby(['item_title','sku_id'])['price'].sum().sort_values(ascending=False)
st.write(gp)