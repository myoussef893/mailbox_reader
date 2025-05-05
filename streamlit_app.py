import streamlit as st 
import pandas as pd 



df = pd.read_sql('amazon_orders',con='sqlite:///app_base.db').dropna()
grouped = df.groupby('sku_id',as_index=False)['sku_id'].count()

st.write(grouped)