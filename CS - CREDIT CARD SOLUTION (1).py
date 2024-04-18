#!/usr/bin/env python
# coding: utf-8

# # DATA EXPLORATORY ANALYSIS FOR CREDIT CARD DATA

# In[5]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt


# In[6]:


## importing data 
cred_card = pd.read_excel('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 2 - Credit Card Case Study/Credit Card Data.xlsx')
Customer = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 2 - Credit Card Case Study/Customer Acqusition.csv')
Repayment = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 2 - Credit Card Case Study/Repayment.csv')
spend = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY/Case Study 2 - Credit Card Case Study/spend.csv')


# In[7]:


Customer


# In[8]:


Repayment.head(2)


# In[9]:


spend.head(2)


# # Following are some of Mr. Watson’s questions to a Consultant (like you) to understand the customers spend & repayment behavior.
# 

# ### 1. In the above dataset,
#  

# ### a. In case age is less than 18, replace it with mean of age values

# In[10]:


Customer['Age'] = np.where(Customer['Age']<18 ,Customer['Age'].mean() , Customer['Age'])


# In[11]:


Customer


# ### b. In case spend amount is more than the limit, replace it with 50% of that customer’s limit. (customer’s limit provided in acquisition table is the per transaction limit on his card)
# 

# In[12]:


customer_spend = pd.merge(spend , Customer , on = 'Customer')
customer_spend


# In[13]:


customer_spend[customer_spend["Amount"] > customer_spend['Limit']]


# In[14]:


customer_spend.loc[customer_spend["Amount"] > customer_spend["Limit"],"Amount"]=(50 * customer_spend["Limit"]).div(100)


# In[15]:


customer_spend[customer_spend["Amount"] > customer_spend['Limit']]


# ### c. Incase the repayment amount is more than the limit, replace the repayment with the limit. 

# In[16]:


Customer.head()


# In[17]:


Customer_repayment = pd.merge(Customer , Repayment , on = 'Customer')
Customer_repayment


# In[18]:


Customer_repayment[Customer_repayment['Amount'] > Customer_repayment['Limit']]


# In[19]:


Customer_repayment.loc[Customer_repayment['Amount'] > Customer_repayment['Limit'] , 'Amount'] = (50 * Customer_repayment['Limit']).div(100)


# In[20]:


Customer_repayment[Customer_repayment['Amount'] > Customer_repayment['Limit']]


# ### 2. From the above dataset create the following summaries:

# ###  a. How many distinct customers exist?

# In[21]:


Customer.Customer.nunique()


# ### b. How many distinct categories exist?
# 

# In[22]:


Customer.Segment.nunique()


# ### c. What is the average monthly spend by customers?

# In[23]:


customer_spend


# In[24]:


customer_spend['Month'] = pd.to_datetime(customer_spend.Month)


# In[25]:


customer_spend['Month_Name'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%B"))
customer_spend['Year'] = customer_spend['Month'].apply(lambda x:pd.Timestamp.strftime(x,format="%Y"))
customer_spend


# In[26]:


#customer_spend['Month_Name'] = customer_spend['Month'].dt.month_name()


# In[27]:


customer_spend.groupby(['Year','Month_Name'])['Amount'].mean().reset_index()


# In[28]:


Avg_spend_by_cust = customer_spend.groupby(['Customer' , 'Month_Name'])['Amount'].mean().reset_index()
Avg_spend_by_cust


# ### d. What is the average monthly repayment by customers?

# In[29]:


Repayment['Month'] = pd.to_datetime(Repayment['Month'] , format = 'mixed')


# In[30]:


Repayment


# In[31]:


Repayment['Month_Name'] = Repayment.Month.dt.month_name()
Repayment['Year'] = Repayment.Month.dt.year
Repayment


# In[32]:


Repayment.groupby(['Year','Month_Name'])['Amount'].mean().reset_index()


# In[33]:


Repayment.groupby(['Customer' , 'Month_Name'])['Amount'].mean().reset_index()


# ### e. If the monthly rate of interest is 2.9%, what is the profit for the bank for each month?
# 
# (Profit is defined as interest earned on Monthly Profit. 
# Monthly Profit = Monthly repayment – Monthly spend. Interest is earned only on positive profits and not on negative amounts)

# In[34]:


customer_spend_repayment = pd.merge(customer_spend , Repayment , on = 'Customer')
customer_spend_repayment.head(2)


# In[35]:


customer_spend_repayment.rename(columns={"Amount_x":"Spend_Amount","Amount_y":"Repay_Amount"},inplace=True)


# In[36]:


Grouped_data = customer_spend_repayment.groupby(['Year_x' , 'Month_Name_x']).agg({'Spend_Amount' : 'sum','Repay_Amount' : 'sum'})
Grouped_data  


# In[37]:


Grouped_data['Monthly_profit'] = Grouped_data['Repay_Amount'] - Grouped_data['Spend_Amount']
Grouped_data


# In[38]:


Grouped_data['Interest_earned'] =(2.9* Grouped_data['Monthly_profit'])/100
Grouped_data


# ### f. What are the top 5 product types?

# In[39]:


customer_spend_repayment['Type'].nunique()


# In[40]:


plt.figure(figsize = (5,3))
customer_spend_repayment['Type'].value_counts().plot(kind = 'bar')
plt.show()


# ### g. Which city is having maximum spend?

# In[41]:


customer_spend_repayment.groupby('City')['Spend_Amount'].sum()


# In[42]:


ex = [0.0,0.0 ,0.0 , 0.0 , 0.0, 0.1 ,0.2 ,0.1]

plt.figure(figsize = (7,7))
customer_spend_repayment.groupby('City')['Spend_Amount'].sum().plot(kind = 'pie' , autopct = '%1.2f%%' , explode = ex , 
                                                                   shadow = True)
plt.title("Amount spended in each city")
plt.legend(bbox_to_anchor=(1.5, 1))
plt.show()


# ### h. Which age group is spending more money?

# In[43]:


customer_spend["Age"].max()


# In[44]:


customer_spend['Age_Group'] =  pd.cut(customer_spend["Age"],bins=np.arange(18,88,8),labels=["18-26","26-34",
                                            "34-42" ,"42-50" ,"50-58","58-66","66-74","74-82"],include_lowest=True)
customer_spend


# In[45]:


customer_spend.groupby('Age_Group')['Amount'].sum()


# In[46]:


exp = [0.0,0.0 ,0.1 , 0.2 , 0.0, 0.0 ,0.0 ,0.0]

plt.figure(figsize = (5,5))
customer_spend.groupby('Age_Group')['Amount'].sum().plot(kind = 'pie' , autopct = '%1.2f%%' , explode = exp ,
                                                                   shadow = True)
plt.title("Amount spended by each age group")
plt.legend(bbox_to_anchor=(1.1, 1))
plt.show()


# ### i. Who are the top 10 customers in terms of repayment?

# In[47]:


customer_spend_repayment.groupby('Customer')['Repay_Amount'].sum().sort_values(ascending = False)


# ### 3. Calculate the city wise spend on each product on yearly basis. Also include a graphical representation for the same.

# In[48]:


Customer_spend_summary = pd.pivot_table(customer_spend , index = ["City","Year"] ,columns='Product'  , 
                                        aggfunc = 'sum' , values = 'Amount')
Customer_spend_summary


# In[49]:


Customer_spend_summary.plot(kind='bar' , width= 0.9 , figsize=(10,5))
plt.ylabel("Spend Amount")
plt.title("Amount spended by customers according to year and city")
plt.show()


# ## 4. Create graphs for

# ###  a. Monthly comparison of total spends, city wise

# In[50]:


Filtered_data = pd.pivot_table(customer_spend,values='Amount',index='Month_Name',columns='City',aggfunc='sum')


# In[51]:


Filtered_data.plot(kind='bar' , width= 0.9 , figsize=(15,5))
plt.title("Monthly comparison of total spends, city wise")
plt.legend(bbox_to_anchor=(1.1, 1))
plt.show()


# ###  b. Comparison of yearly spend on air tickets

# In[52]:


customer_spend['Type'].unique()


# In[53]:


Filtered = customer_spend.groupby(["Year","Type"])[["Amount"]].sum().reset_index()


# In[54]:


Filtered_airtickets =Filtered[Filtered['Type']== 'AIR TICKET']
Filtered_airtickets


# In[55]:


plt.bar(Filtered_airtickets["Year"],height=Filtered_airtickets["Amount"])
plt.xlabel("Year")
plt.ylabel("Amount Spent")
plt.title("Comparison of yearly spend on air tickets")
plt.show()


# ### c. Comparison of monthly spend for each product (look for any seasonalitythat exists in terms of spend

# In[56]:


monthly_spend = pd.pivot_table(customer_spend , index = 'Month_Name' , columns = 'Product' , values='Amount' , aggfunc = 'sum')
monthly_spend


# In[57]:


monthly_spend.plot(kind = 'bar' , figsize = (10,5))
plt.title('Comparison of monthly spend for each product')
plt.show()

print('''We can see from the above graph that the spend amounts are high for all the Products during  January 
, February and March.''')


# ### 5. Write user defined PYTHON function to perform the following analysis:
# You need to find top 10 customers for each city in terms of their repayment amount by 
# different products and by different time periods i.e. year or month. The user should be able 
# to specify the product (Gold/Silver/Platinum) and time period (yearly or monthly) and the 
# function should automatically take these inputs while identifying the top 10 customers.

# In[58]:


Customer_repayment['Month'] = pd.to_datetime(Customer_repayment['Month'])


# In[59]:


Customer_repayment['Month_Name'] = Customer_repayment['Month'].apply(lambda x : pd.Timestamp.strftime(x,format='%B'))
Customer_repayment['Year'] = Customer_repayment['Month'].apply(lambda x : pd.Timestamp.strftime(x,format = '%Y'))
Customer_repayment


# In[93]:


Customer_repayment.Product.unique()


# In[100]:


def Top_10_customers( Product , time_period):
    print('Give the product name and timeperiod for which you want the data')
    
    if Product.lower()=='gold' and time_period.lower()=='monthly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Gold'].groupby([ 'Product' , 'Customer' , 'Month_Name' ,
             'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)
    
    elif Product.lower()=='gold' and time_period.lower()=='yearly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Gold'].groupby([ 'Product' , 'Customer' , 'Year' ,
             'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)
        
    elif Product.lower()=='silver' and time_period.lower()=='monthly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Silver'].groupby([ 'Product' , 'Customer' , 'Month_Name'
            ,'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)
    
    elif Product.lower()=='silver' and time_period.lower()=='yearly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Silver'].groupby([ 'Product' , 'Customer' , 'Month_Name'
            ,'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)
    
    elif Product.lower()=='platimum' and time_period.lower()=='monthly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Platimum'].groupby([ 'Product' , 'Customer' , 'Month_Name'
            ,'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)
    
    elif Product.lower()=='platimum' and time_period.lower()=='yearly':
        
        return  Customer_repayment[Customer_repayment['Product'] == 'Platimum'].groupby([ 'Product' , 'Customer' , 'Month_Name'
            ,'City' ])['Amount'].sum().sort_values(ascending = False).reset_index().head(10)


# In[101]:


Top_10_customers( 'platimum' , 'yearly')


# In[ ]:




