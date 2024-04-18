#!/usr/bin/env python
# coding: utf-8

# # E-Commerce Market Place Company 

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


# In[2]:


CUSTOMERS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/CUSTOMERS.csv')
GEO_LOCATION = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/GEO_LOCATION.csv')
ORDER_ITEMS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/ORDER_ITEMS.csv')
ORDER_PAYMENTS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/ORDER_PAYMENTS.csv')
ORDER_REVIEWS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/ORDER_REVIEW_RATINGS.csv')
ORDERS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/ORDERS.csv')
PRODUCTS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/PRODUCTS.csv')
SELLERS = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/E-Commerce Analytics Project/SELLERS.csv')


# In[3]:


CUSTOMERS.head(2)


# In[4]:


GEO_LOCATION.head(2)


# In[5]:


ORDER_ITEMS.head(2)


# In[6]:


ORDER_PAYMENTS.head(2)


# In[7]:


ORDER_REVIEWS.head(2)


# In[8]:


ORDERS.head(2)


# In[9]:


PRODUCTS.head(2)


# In[10]:


SELLERS.head(2)


# In[11]:


Final_data = pd.merge(pd.merge(CUSTOMERS , GEO_LOCATION , left_on = 'customer_zip_code_prefix' ,right_on = 
                     'geolocation_zip_code_prefix' ) , ORDERS , on = 'customer_id')

Final_data.drop(columns = ['geolocation_city' , 'geolocation_state' ,  'geolocation_zip_code_prefix'] , inplace = True)


# In[12]:


Final_data = pd.merge(pd.merge(Final_data , ORDER_ITEMS , on = 'order_id') , ORDER_REVIEWS , on= 'order_id')


# In[13]:


Final_data= pd.merge(pd.merge(Final_data , ORDER_PAYMENTS , on= 'order_id' , how = 'inner') , 
                    PRODUCTS , on = 'product_id')


# In[14]:


Final_data = pd.merge(Final_data , SELLERS , on = 'seller_id')


# In[15]:


Final_data.info()


# In[16]:


Final_data.order_delivered_carrier_date = pd.to_datetime(Final_data.order_delivered_carrier_date , format = '%m/%d/%Y %H:%M')
Final_data.order_delivered_customer_date = pd.to_datetime(Final_data.order_delivered_customer_date , format = '%m/%d/%Y %H:%M')
Final_data.order_estimated_delivery_date = pd.to_datetime(Final_data.order_estimated_delivery_date , format = '%m/%d/%Y %H:%M')
Final_data.shipping_limit_date = pd.to_datetime(Final_data.shipping_limit_date , format = '%m/%d/%Y %H:%M')
Final_data.review_creation_date = pd.to_datetime(Final_data.review_creation_date , format = '%m/%d/%Y %H:%M')
Final_data.order_purchase_timestamp = pd.to_datetime(Final_data.order_purchase_timestamp , format = '%m/%d/%Y %H:%M')


# In[17]:


Final_data.select_dtypes('datetime64')


# ## 1. Perform Detailed exploratory analysis

# ### a. Define & calculate high level metrics like (Total Revenue, Total quantity, Total products, Total categories, Total sellers, Total locations, Total channels, Total payment methods etc…) 

# In[18]:


print('Total Revenue : ' , Final_data['payment_value'].sum())
print('Total Quantity : ' ,Final_data['order_item_id'].count())
print('Total Products : ' ,Final_data['product_id'].nunique())
print('Total No. of Customers : ' , Final_data['customer_id'].nunique())
print('Total Categories : ' , Final_data['product_category_name'].nunique())
print('Total Sellers : ' , Final_data['seller_id'].nunique())
print('Total Locations  : ' , Final_data['customer_zip_code_prefix'].nunique())
print('Total No. of City : ' ,Final_data['customer_city'].nunique())
print('Total No. of state : ' , Final_data['customer_state'].nunique())
print('Total Payment methods : ' , Final_data['payment_type'].nunique())


# ### b. Understanding how many new customers acquired every month

# In[19]:


Final_data['Month'] = Final_data.order_purchase_timestamp.dt.strftime('%B')
Final_data['Year'] = Final_data.order_purchase_timestamp.dt.strftime('%Y')


# In[20]:


Final_data[~Final_data.customer_id.duplicated()].groupby(['Year' , 'Month'])['customer_id'].count()


# In[21]:


Final_data


# ### c. Understand the retention of customers on month on month basis

# In[22]:


Final_data[Final_data.customer_id.duplicated()].groupby(['Year' , 'Month'])['customer_id'].count()


# ### d. How the revenues from existing/new customers on month on month basis

# In[23]:


Final_data['Month_no'] = Final_data['order_purchase_timestamp'].dt.strftime('%m')


# In[24]:


pd.concat([
    Final_data[Final_data.customer_id.duplicated()].groupby(['Year' ,'Month_no'])['payment_value'].sum().rename('existing'),
    Final_data[~Final_data.customer_id.duplicated()].groupby(['Year' , 'Month_no' ])['payment_value'].sum().rename('new')],
    axis=1,sort=True) 


# ### e. Understand the trends/seasonality of sales, quantity by category, location, month, week, day, time, channel, payment method etc…

# In[25]:


Final_data['Week'] = Final_data['order_purchase_timestamp'].dt.strftime('%W')
Final_data['Day'] = Final_data['order_purchase_timestamp'].dt.strftime('%d')


# In[26]:


#Quantity by category

Qty_by_cat = Final_data.groupby('product_category_name')['order_item_id'].count().sort_values(ascending = False)
Qty_by_cat


# In[27]:


Qty_by_cat.sort_values().plot(kind='barh' , figsize = (5,14) , color = 'g')
plt.ylabel('Quantity')
plt.title('Quantity by Category')
plt.show()


# In[28]:


#Quantity by Location

Final_data.groupby(['customer_city'])['order_item_id'].count().sort_values(ascending = False)


# In[29]:


#Quantity by Month

Final_data.groupby(['Month'])['order_item_id'].count().sort_values(ascending = False)


# In[30]:


Final_data.groupby(['Month'])['order_item_id'].count().sort_values(ascending = False).plot(kind = 'barh' , figsize = (8,5))
plt.ylabel('Quantity')
plt.title('Quantity by Month')
plt.show()


# In[31]:


#Quantity by Week

Final_data.groupby(['Week'])['order_item_id'].count().sort_index()


# In[32]:


#Quantity by Day

Final_data.groupby(['Day'])['order_item_id'].count().sort_index()


# In[33]:


#Quantity by year and month

Final_data.groupby(['Year' ,'Month'])['order_item_id'].count().sort_index()


# In[34]:


Final_data.groupby(['Year' ,'Month'])['order_item_id'].count().sort_index().plot(kind='bar' , figsize = (8,5))
plt.ylabel('Quantity')
plt.title('Quantity by Year and month')
plt.show()


# In[35]:


Final_data.groupby(['payment_type'])['order_item_id'].count()


# In[36]:


ex = [0.0 , 0.0 , 0.2 , 0.2]
Final_data.groupby(['payment_type'])['order_item_id'].count().plot(kind = 'pie' , autopct ='%1.1f%%' , 
                                                                   explode = ex , shadow = True)
plt.title('Quantity by Payment types')
plt.show()


# ### f. Popular Products by month, seller, state, category

# In[37]:


Pop_prod_YM = Final_data.groupby(['Year','Month','product_id']).order_id.count().rename('count').reset_index()

Pop_prod_YM.sort_values(['Year', 'count'], ascending=[True,False]).drop_duplicates(['Year','Month']).reset_index(drop=True)


# In[38]:


Pop_prod_seller = Final_data.groupby(['seller_id','product_id']).order_id.count().rename('count').reset_index()

Pop_prod_seller.sort_values(['count'] , ascending = False).drop_duplicates(['seller_id']).reset_index(drop=True)


# In[39]:


Pop_prod_state = Final_data.groupby(['customer_state','product_id']).order_id.count().rename('count').reset_index()
Pop_prod_state.sort_values(['count'] , ascending = False).drop_duplicates('customer_state').reset_index(drop=True)


# In[40]:


Pop_prod_cat = Final_data.groupby(['product_category_name','product_id']).order_id.count().rename('count').reset_index()
Pop_prod_cat.sort_values(['count'] , ascending = False).drop_duplicates('product_category_name').reset_index(drop=True)


# ### g. Popular categories by state, month
# 

# In[41]:


Pop_cat_state = Final_data.groupby(['customer_state','product_category_name']).order_id.count().rename('count').reset_index()

Pop_cat_state.sort_values(['count'] , ascending = False).drop_duplicates('customer_state').reset_index(drop=True)


# In[42]:


Pop_cat_month = Final_data.groupby(['Month','product_category_name']).order_id.count().rename('count').reset_index()
Pop_cat_month.sort_values(['count'] , ascending = False).drop_duplicates('Month').reset_index(drop=True)


# ### h. List top 10 most expensive products sorted by price

# In[43]:


Final_data[['product_category_name' ,'price']].sort_values( by = 'price' , ascending = False).head(10)


# ## 2. Performing Customers/sellers Segmentation

# ### a. Divide the customers into groups based on the revenue generated 

# In[76]:


Customer_by_Rev = Final_data.groupby('customer_id')['payment_value'].sum().sort_values(ascending=False).reset_index()
Customer_by_Rev


# In[77]:


Customer_by_Rev['Revenue'] = np.where(Customer_by_Rev.payment_value >500 , 'High' , np.where(
    Customer_by_Rev.payment_value > 100 , 'Medium' ,'Low' ))


# In[78]:


Customer_by_Rev.groupby('Revenue')['customer_id'].count()


# ### b. Divide the sellers into groups based on the revenue generated

# In[82]:


Seller_by_Rev.payment_value.mean()


# In[65]:


Seller_by_Rev = Final_data.groupby('seller_id')['payment_value'].sum().sort_values(ascending=False).reset_index()
Seller_by_Rev


# In[72]:


Seller_by_Rev['Revenue'] = np.where(Seller_by_Rev.payment_value >5000 , 'High' , np.where(
    Seller_by_Rev.payment_value > 500 , 'Medium' ,'Low' ))


# In[74]:


Seller_by_Rev.groupby('Revenue')['seller_id'].count()


# ### 3. Cross-Selling (Which products are selling together)
# Hint: We need to find which of the top 10 combinations of products are selling together in 
# each transaction. (combination of 2 or 3 buying together

# In[ ]:





# In[ ]:





# In[ ]:





# ## 4. Payment Behaviour

# ### a. How customers are paying?

# In[85]:


Final_data.groupby([ 'payment_type' , 'payment_installments'])['customer_id'].count().reset_index()


# ### b. Which payment channels are used by most customers?
# 

# In[91]:


Channel_payments = Final_data.groupby([ 'payment_type'])['customer_id'].count().sort_values(ascending=False)
Channel_payments


# In[93]:


Channel_payments.plot(kind='bar')
plt.title('Payment channels by count of Customers')
plt.ylabel('Count of Customers')
plt.show()


# ## 5. Customer satisfaction towards category & product

# ### a. Which categories (top 10) are maximum rated & minimum rated?
# 

# In[106]:


Top_10_cat = Final_data.groupby('product_category_name')['review_score'].agg(['mean' , 'count']).sort_values(by='count' ,
                                                                                ascending = False).head(10)


# In[105]:


Top_10_cat.sort_values(by = 'mean' , ascending = False).drop(columns = 'count')


# ### b. Which products (top10) are maximum rated & minimum rated?

# In[108]:


Top_10_prod = Final_data.groupby('product_id')['review_score'].agg(['mean' , 'count']).sort_values(by='count' ,
                                                                                ascending = False).head(10)


# In[109]:


Top_10_prod.sort_values(by = 'mean' , ascending = False).drop(columns = 'count')


# ### c. Average rating by location, seller, product, category, month etc.

# In[114]:


Final_data.groupby('customer_city')['review_score'].mean().sort_values(ascending = False)


# In[115]:


Final_data.groupby('customer_state')['review_score'].mean().sort_values(ascending = False)


# In[116]:


Final_data.groupby('Month')['review_score'].mean().sort_values(ascending = False)


# In[117]:


Final_data.groupby('Year')['review_score'].mean().sort_values(ascending = False)


# In[ ]:





# In[ ]:




