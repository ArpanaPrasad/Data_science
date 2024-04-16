#!/usr/bin/env python
# coding: utf-8

# # CASE STUDY : CUSTOMER ANALYSIS FOR RETAIL
# 

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime


# In[ ]:





# In[5]:


customer = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 1 - Retail Case Study/Customer.csv')
transaction = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 1 - Retail Case Study/Transactions.csv')
product_cat_info = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 1 - Retail Case Study/prod_cat_info.csv')


# In[6]:


customer


# In[7]:


transaction


# In[8]:


product_cat_info


# ### 1. Merge the datasets Customers, Product Hierarchy and Transactions as Customer_Final. Ensure to keep all customers who have done transactions with us and select the join type accordingly. 

# In[9]:


join_cust_transaction = pd.merge( transaction , customer , left_on='cust_id' , right_on='customer_Id' , how = 'left')


# In[10]:


join_cust_transaction.head()


# In[11]:


Customer_Final = pd.merge(join_cust_transaction , product_cat_info , on = 'prod_cat_code')


# In[12]:


Customer_Final


# ### Prepare a summary report for the merged data set.
# a. Get the column names and their corresponding data types

# In[13]:


Customer_Final.dtypes


# #### b. Top/Bottom 10 observations 

# In[14]:


Customer_Final.head(10)


# #### c. “Five-number summary” for continuous variables (min, Q1, median, Q3 and max)

# In[15]:


Summary = Customer_Final.describe().T


# In[16]:


Summary


# #### d. Frequency tables for all the categorical variables

# In[17]:


catagorical_Final = Customer_Final.select_dtypes('object')


# In[18]:


catagorical_Final


# In[19]:


Frequency_table = catagorical_Final.groupby(['tran_date' ,'Store_type' , 'Gender' , 'prod_cat']).size().reset_index(name = 'Count')


# In[20]:


Frequency_table


# ### 3. Generate histograms for all continuous variables and frequency bars for categorical variables

# In[21]:


Customer_Final.select_dtypes('number').hist(figsize = ( 20 ,15))
plt.show()


# In[22]:


for column in catagorical_Final:    
    sns.countplot(x=column, data=catagorical_Final)
    plt.show()


# ### 4. Calculate the following information using the merged dataset :
# a. Time period of the available transaction data

# In[26]:


Customer_Final


# In[29]:


Customer_Final['tran_date'] = pd.to_datetime(Customer_Final['tran_date'] ,  format = 'mixed')


# In[30]:


oldest_date = Customer_Final.tran_date.min()
latest_date = Customer_Final.tran_date.max()

print(oldest_date)
print(latest_date)


# In[31]:


Time_period_years = latest_date.year - oldest_date.year
Time_period_days = latest_date - oldest_date

print('Time period of transaction in years' , Time_period_years)
print('Time period of transaction in days' , Time_period_days)


# #### b. Count of transactions where the total amount of transaction was negative

# In[32]:


Customer_Final.loc[Customer_Final.total_amt < 0,['total_amt']].count()


# ### 5. Analyze which product categories are more popular among females vs male customers.

# In[33]:


pd.pivot_table(Customer_Final , values = 'transaction_id' , index = 'Gender' , columns = 'prod_cat' , aggfunc = 'count')


# ### 6. Which City code has the maximum customers and what was the percentage of customers from that city?

# In[34]:


Cust_by_city = Customer_Final.groupby('city_code')['customer_Id'].count().sort_values(ascending=False)


# In[35]:


max_customers_city = Cust_by_city.idxmax()
print(max_customers_city)


# In[36]:


percentage_of_cust = (Cust_by_city[max_customers_city] / len(Customer_Final.city_code)) * 100
print(percentage_of_cust)


# ### 7. Which store type sells the maximum products by value and by quantity?

# In[37]:


Max_value_Sold_by_store = Customer_Final.Store_type.value_counts().sort_values(ascending=False).iloc[0:1]
Max_value_by_Quantity = Customer_Final.Qty.value_counts().sort_values(ascending=False).iloc[0:1]

print(Max_value_Sold_by_store)
print(Max_value_by_Quantity)


# ### 8. What was the total amount earned from the "Electronics" and "Clothing" categories from Flagship Stores?

# In[38]:


amt_erned_by_cat = Customer_Final.groupby(['prod_cat' ,'Store_type'])['total_amt'].sum().reset_index(name='Sum_of_amt')


# In[39]:


amt_erned_by_cat[(amt_erned_by_cat.Store_type == 'Flagship store') & (amt_erned_by_cat['prod_cat'].isin(['Electronics', 'Clothing']))]


# ### 9. What was the total amount earned from "Male" customers under the "Electronics" category?

# In[40]:


amt_erned_byeach_cat_and_Gender  = Customer_Final.groupby(['Gender' ,'prod_cat'])['total_amt'].sum().reset_index(name='Sum_of_amt')


# In[41]:


amt_erned_byeach_cat_and_Gender[(amt_erned_byeach_cat_and_Gender.Gender == 'M') &  (amt_erned_byeach_cat_and_Gender.prod_cat == 'Electronics')]


# ### 10. How many customers have more than 10 unique transactions, after removing all transactions  which have any negative amounts?

# In[42]:


Filtered_data = Customer_Final[Customer_Final['total_amt'] >= 0]


# In[43]:


unique_transactions_Count = Filtered_data.groupby('cust_id')['transaction_id'].nunique()


# In[44]:


unique_transactions_Count[unique_transactions_Count>10].count()


# ### 11. For all customers aged between 25 - 35, find out:
# 

# ### a. What was the total amount spent for “Electronics” and “Books” product categories?

# In[45]:


amt_erned_by_prod_cat = Customer_Final.groupby('prod_cat')['total_amt'].sum().round(2).reset_index()


# In[46]:


amt_erned_by_prod_cat[amt_erned_by_prod_cat['prod_cat'].isin(['Electronics','Books'])]


# ### b. What was the total amount spent by these customers between 1st Jan, 2014 to 1st Mar, 2014?

# In[47]:


Filtered_by_date = Customer_Final[(Customer_Final['tran_date'] >= '2014-01-01') & (Customer_Final['tran_date'] < '2014-03-01')]


# In[48]:


Filtered_by_date['total_amt'].sum()


# In[ ]:





# In[ ]:




