from imap_tools import MailBox,AND
import pandas as pd 
import re

usr = 'muhammad.yousef7489@gmail.com'
pwd = 'qozf nxkh tnve bpad'


def extract(term, text):
    try:
        match = re.search(term, text)
        return match.group(1) if match else None  # Return None if no match is found
    except Exception as e:
        print(f"Error during extraction for term '{term}': {e}")
        return None  # Return None in case of any other error during regex operation

with MailBox('imap.gmail.com',port=993).login(username=usr,password=pwd) as mailbox: 
    mailbox.folder.set('Amazon/Sales')
    fetcher = mailbox.fetch(AND(subject='Sold'),reverse=True, limit=500)
    
    try:  
        all_orders = []
        for message in fetcher: 
            order_dict = {}
            order_dict['order_date'] = str(message.date)
            order_dict['order_id'] = extract(r'<b>Order ID:</b>(.*?)\r\n',message.html)
            order_dict['shipping_type'] = extract(r'<b>Please ship this order using:</b>(.*?)\r\n',message.html)
            order_dict['cod_prepaid'] = extract(r'<b>Collect on Delivery prepaid:</b> EGP(.*?)\r\n',message.html)
            order_dict['cod_amount'] = extract(r'<b>Collect on Delivery amount:</b> EGP(.*?)\r\n',message.html)
            order_dict['max_shipping_date'] = extract(r'<b>Ship by:</b>(.*?)\r\n',message.html)
            order_dict['item_title'] = extract(r'<b>Item:</b>(.*?)\r\n',message.html)
            order_dict['condition'] = extract(r'<b>Condition:</b>(.*?)\r\n',message.html)
            order_dict['sku_id'] = extract(r'<b>SKU:</b>(.*?)\r\n',message.html)
            order_dict['quantity'] = extract(r'<b>Quantity:</b>(.*?)\r\n',message.html)
            order_dict['price'] = extract(r'<b>Price:</b> EGP(.*?)\r\n',message.html)      
            order_dict['Shipping_fees'] = extract(r'<b>Shipping:</b> EGP(.*?)\r\n',message.html)
            order_dict['amazon_fees'] = extract(r'<b>Amazon fees:</b> -EGP(.*?)\r\n',message.html)
            order_dict['cod_fees'] = extract(r'<b>Collect on Delivery fees:</b> EGP(.*?)\r\n',message.html)
            all_orders.append(order_dict)
            print(f'Success, Order ID: {order_dict['order_id']}')
        
        df = pd.DataFrame(all_orders) 
        df.to_sql('amazon_orders',con='sqlite:///app_base.db',if_exists='replace')
    except Exception as e: 
        print(e)