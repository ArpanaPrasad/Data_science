#!/usr/bin/env python
# coding: utf-8

# # CASE STUDY : Visualizations in Python on Sales Data
# 

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns


# In[2]:


SalesData = pd.read_csv('D:/ANALYTICS TERM_2/CASE_STUDY/Case Study 4 - Python Visualizations Case Study/SalesData.csv')


# In[3]:


SalesData.head(2)


# ### 1. Compare Sales by region for 2016 with 2015 using bar chart

# In[4]:


Filtered_Sales = SalesData.groupby('Region')[['Sales2016' , 'Sales2015']].sum().round().reset_index()


# In[5]:


Filtered_Sales


# In[6]:


plt.bar( Filtered_Sales.Region , Filtered_Sales.Sales2016 ,  color = 'yellow' , label = 'Sales2016' )
plt.bar( Filtered_Sales.Region , Filtered_Sales.Sales2015 ,bottom = Filtered_Sales.Sales2015 , color = 'green' ,label = 'Sales2015' )
plt.legend()
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()


# In[7]:


width = 0.4
xaxis_values = np.arange(len(Filtered_Sales.Region))

plt.bar( xaxis_values, Filtered_Sales.Sales2016 , width = 0.4 , color = 'yellow' , label = 'Sales2016' )
plt.bar( xaxis_values + width, Filtered_Sales.Sales2015 ,width , color = 'green' ,label = 'Sales2015' )
plt.legend()
plt.xlabel('Region')
plt.ylabel('Sales')
plt.xticks(xaxis_values + width/2 , Filtered_Sales.Region)
plt.show()


# In[8]:


Filter_Data= SalesData.groupby('Region')[['Sales2016' , 'Sales2015']].sum().round()


# In[9]:


Filter_Data.plot(kind='bar' , figsize = (4,4))
plt.xlabel('Region')
plt.ylabel('Sales')
plt.show()


# ### 2. Pie charts for sales for each region in 2016

# In[10]:


Filter_Data.Sales2016.plot(kind = 'pie' ,  autopct = '%1.1f%%')
plt.title('Sales  by Region in 2016')
plt.show()


# In[11]:


plt.pie(Filtered_Sales.Sales2016 , labels = Filtered_Sales.Region , autopct = '%1.1f%%') 
plt.title('Sales  by Region in 2016')
plt.show()


# ### 3. Compare sales of 2015 and 2016 with Region and Tiers

# In[12]:


Filter_SalesandTier = SalesData.groupby(['Region','Tier'])[['Sales2016' , 'Sales2016' ]].sum().round(2)
Filter_SalesandTier


# In[13]:


Filter_SalesandTier.plot(kind="bar",figsize=(4,4))
plt.ylabel("Sales")
plt.title("Total sales of 2015 and 2016 with respect to Region and Tiers")
plt.show()


# ### 4. In East region, which state registered a decline in 2016 as compared to 2015? 

# In[14]:


sales_state = SalesData.groupby(['Region',"State"])['Sales2015','Sales2016'].sum().round()
sales_state.head()


# In[15]:


east_sales = sales_state.loc['East']
east_sales


# In[16]:


east_sales.plot(kind = 'bar')
plt.title("Sales comparison between 2015 and 2016 for East Region")
plt.show()


# ### 5. In all the High tier, which Division saw a decline in number of units sold in 2016 compared to  2015 ?

# In[17]:


Sales_division_Tier = SalesData.groupby(['Tier' , 'Division'])[['Units2015' , 'Units2016']].sum()
Sales_division_Tier.head()


# In[18]:


High_Tier = Sales_division_Tier.loc['High']
High_Tier.head()


# In[19]:


High_Tier.plot(kind = 'bar' , figsize = (8 , 4) )
plt.title('units sold in 2016 compared to 2015')
plt.show()

print('No division show decline in number of units sold in 2016 compared to 2015')


# ### 7. Compare Qtr wise sales in 2015 and 2016 in a bar plot

# In[20]:


Month = SalesData['Month']
Month


# In[21]:


Qtr = []

for x in Month:
    if x in ['Jan' , 'Feb' , 'Mar']:
        Qtr.append('Q1')
    elif x in ['Apr' , 'May' , 'Jun']:
        Qtr.append('Q2')
    elif x in ['Jul' , 'Aug' , 'Sep']:
        Qtr.append('Q3')
    else:
        Qtr.append('Q4')

Qtr


# In[22]:


SalesData['Qtr'] = pd.Series(Qtr)
SalesData


# In[23]:


##Compare Qtr wise sales in 2015 and 2016 in a bar plot
Quterly_sales = SalesData.groupby('Qtr')[['Sales2015' , 'Sales2016']].sum().round()


# In[24]:


Quterly_sales.plot(kind = 'bar')
plt.title('Quterly sales 2015 Compared to 2016 ')
plt.show()


# ### 8. Determine the composition of Qtr wise sales in and 2016 with regards to all the Tiers in a pie chart. (Draw 4 pie charts representing a Quarter for each Tier)

# In[25]:


Qtr_tier_Sales = SalesData.pivot_table(index='Qtr',columns='Tier',values='Sales2016')
Qtr_tier_Sales


# In[26]:


plt.pie(Qtr_tier_Sales.loc['Q1'] , autopct='%1.0f%%' , labels = ['High','Low','Med','Out'])
plt.title('Q1 Sales in 2016 in all Tiers')


# In[27]:


plt.pie(Qtr_tier_Sales.loc['Q2' , :] , autopct='%1.0f%%' , labels = ['High','Low','Med','Out'])
plt.title('Q2 Sales in 2016 in all Tiers')


# In[28]:


plt.pie(Qtr_tier_Sales.loc['Q3' , :].abs() , autopct='%1.0f%%' , labels = ['High','Low','Med','Out'])
plt.title('Q3 Sales in 2016 in all Tiers')


# In[29]:


plt.pie(Qtr_tier_Sales.loc['Q4' , :] , autopct='%1.0f%%' , labels = ['High','Low','Med','Out'])
plt.title('Q4 Sales in 2016 in all Tiers')


# In[ ]:




