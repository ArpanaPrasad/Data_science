#!/usr/bin/env python
# coding: utf-8

# # INSURANCE CLAIMS CASE STUDY

# In[2]:


# import

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime , timedelta

import scipy.stats as stats


# ### 1. Import claims_data.csv and cust_data.csv which is provided to you and combine the two datasets appropriately to create a 360-degree view of the data. Use the same for the subsequent questions.

# In[3]:


claims = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY//Case Study 3 - Insurance Claims Case Study/claims.csv')
cust_data = pd.read_csv('C:/Analytics/Analytics_T_2.1/Python/CASE_STUDY//Case Study 3 - Insurance Claims Case Study/cust_demographics.csv')


# In[4]:


claims.head(2)


# In[5]:


cust_data.head(2)


# In[6]:


claims.rename(columns ={'customer_id' : 'CUST_ID'} , inplace = True)


# In[7]:


Final_data = pd.merge(claims , cust_data , on = 'CUST_ID')


# In[8]:


Final_data.head(2)


# ### 2. Perform a data audit for the datatypes and find out if there are any mismatch within the current datatypes of the columns and their business significance

# In[9]:


Final_data.info()


# ### 3. Convert the column claim_amount to numeric. Use the appropriate modules/attributes to remove the $ sign.

# In[10]:


Final_data['claim_amount'] = pd.to_numeric(Final_data['claim_amount'].replace('[\$,]' , '' , regex=True))


# In[11]:


Final_data.info()


# ### 4. Of all the injury claims, some of them have gone unreported with the police. Create an alert flag (1,0) for all such claims.

# In[12]:


Final_data['Unreported_claims'] = Final_data['police_report'].replace({'Yes' : 0 , "No" : 1 , "Unknown" : 1})


# In[13]:


Final_data.head(2)


# ### 5. One customer can claim for insurance more than once and in each claim,multiple categories of claims can be involved. However, customer ID should remain unique. 

# In[14]:


len(Final_data.groupby('CUST_ID').agg({
    'claim_amount': 'sum',
    'claim_area': lambda x: ','.join(x.unique()),}))


# In[15]:


Final_data.sort_values(by=['CUST_ID', 'claim_date'] , ascending = [True , True ] , inplace = True)


# In[16]:


Final_data = Final_data.drop_duplicates('CUST_ID', keep='first')


# In[17]:


Final_data.info()


# ### 6. Check for missing values and impute the missing values with an appropriate value. (mean for continuous and mode for categorical)

# In[18]:


Final_data.isnull().sum()


# In[19]:


Final_data['claim_amount'] = Final_data['claim_amount'].fillna(Final_data['claim_amount'].mean())


# In[20]:


Final_data['total_policy_claims']= Final_data['total_policy_claims'].fillna(Final_data['total_policy_claims'].mean())


# ### 7. Calculate the age of customers in years. Based on the age, categorize the
# customers according to the below criteria
# `Children < 18`
# `Youth 18-30`
# `Adult 30-60`
# `Senior > 60`

# In[21]:


curr_year = pd.to_datetime('today').year
dob_year = pd.DatetimeIndex(Final_data['DateOfBirth']).year #extract year from DateOfBirth
x = dob_year-100                                             
v = curr_year - x
y = curr_year - dob_year
Final_data['age'] = (np.where(dob_year > curr_year,v,y))

#Categorising
Final_data.loc[(Final_data.age < 18),'AgeGroup'] = 'Children'
Final_data.loc[(Final_data.age >=18) & (Final_data.age <30),'AgeGroup'] = 'Youth'
Final_data.loc[(Final_data.age >=30) & (Final_data.age <60),'AgeGroup'] = 'Adult'
Final_data.loc[(Final_data.age >=60),'AgeGroup'] = 'Senior'


# In[22]:


Final_data.head(2)


# In[23]:


Final_data.groupby('AgeGroup')['age'].count()


# ### 8. What is the average amount claimed by the customers from various segments?

# In[24]:


Final_data.groupby('Segment')['claim_amount'].agg('mean').round(2)


# ### 9. What is the total claim amount based on incident cause for all the claimsthat have been done at least 20 days prior to 1st of October, 2018.

# In[25]:


Final_data['claim_date'] = pd.to_datetime(Final_data['claim_date'] )


# In[26]:


Total_Claim_Amount = Final_data.loc[Final_data.claim_date < '2018-09-10',:].groupby("incident_cause")["claim_amount"].sum().add_prefix("total_").reset_index(name = 'Claim_Amount')
Total_Claim_Amount


# ### 10. How many adults from TX, DE and AK claimed insurance for driver related issues and causes?

# In[27]:


##Cust_claims.loc[(Cust_claims.incident_cause.str.lower().str.contains("driver") & 
##(Cust_claims.State== "TX") | (Cust_claims.State== "DE") | (Cust_claims.State== "AK")) ]
##.groupby(["State"])["claim_amount"].count()


# In[28]:


AdultS_Claim_Count = Final_data.loc[Final_data.AgeGroup.str.contains('Adult') & (Final_data.incident_cause.str.contains('driver')
                & (Final_data.State == 'TX') | (Final_data.State == 'DE') |
                (Final_data.State == 'AK'))].groupby('State')['claim_amount'].count()

AdultS_Claim_Count


# ### 11. Draw a pie chart between the aggregated value of claim amount based on gender and segment. Represent the claim amount as a percentage onthe pie chart.

# In[29]:


Claim_gender_segment = Final_data.groupby(['gender','Segment'])['claim_amount'].sum().round().reset_index()


# In[30]:


Filtered_gender_seg = Claim_gender_segment.pivot(index="Segment", columns= "gender", values= "claim_amount")
Filtered_gender_seg 


# In[31]:


ex = [0.1 , 0.0]
Filtered_gender_seg.T.plot(kind = "pie" , explode = ex , subplots=True , figsize = (15,10) , autopct='%1.1f%%' , 
                          shadow = True)
plt.show()


# ### 12. Among males and females, which gender had claimed the most for any type of driver related issues? E.g. This metric can be compared using a bar chart

# In[32]:


Gender_driver_claims = Final_data.loc[Final_data.incident_cause.str.contains('driver')].groupby('gender')['claim_amount'].sum()
Gender_driver_claims


# In[33]:


c = ['g' , 'y']
Gender_driver_claims.plot(kind = 'bar' , figsize = (5,4) , color = c)
plt.title('Amount claimed for driver related issue by gender')
plt.show()


# ### 13. Which age group had the maximum fraudulent policy claims? Visualize it on a bar chart.

# In[34]:


Fradulent_policy_claims = Final_data[Final_data.fraudulent == 'Yes'].groupby('AgeGroup')['fraudulent'].count().sort_values(ascending = False)
Fradulent_policy_claims


# In[35]:


Fradulent_policy_claims.plot(kind='bar')
plt.title('Fradulent Policy Claims')
plt.show()
print('Adults had the maximum fraudulent policy claims')


# ### 14. Visualize the monthly trend of the total amount that has been claimed by the customers. Ensure that on the “month” axis, the month is in a chronological order not alphabetical order. 

# In[36]:


Final_data['Claim_month'] = Final_data.claim_date.dt.month
Final_data.head(2)


# In[37]:


Monthly_claims = Final_data.pivot_table(index='Claim_month' , values='claim_amount' , aggfunc = 'sum')


# In[38]:


Monthly_claims.plot(kind='bar')
plt.title('Monthly Claims by Customers')
plt.show()


# ### 15. What is the average claim amount for gender and age categories and suitably represent the above using a facetted bar chart, one facet that represents fraudulent claims and the other for non-fraudulent claims.

# In[39]:


fradulent_policy_claims = Final_data[Final_data.fraudulent == 'Yes'].groupby([ 'gender' , 'AgeGroup']
                )['claim_amount'].mean().round().sort_values(ascending = False)
fradulent_policy_claims


# In[40]:


Non_fradulent_policy_claims = Final_data[Final_data.fraudulent == 'No'].groupby([ 'gender' , 'AgeGroup']
                        )['claim_amount'].mean().round().sort_values(ascending = False)
Non_fradulent_policy_claims


# In[41]:


Claims_age_gender = pd.merge(fradulent_policy_claims,Non_fradulent_policy_claims, on=["gender","AgeGroup"])
Claims_age_gender


# In[42]:


Claims_age_gender = Claims_age_gender.rename(columns={'claim_amount_x' : 'Fraud_policy_claims' , 'claim_amount_y' : 'Non_Fraud_policy_claims' })


# In[43]:


Claims_age_gender.plot(kind='bar' , subplots = True )
plt.show()


# In[44]:


Claims_age_gender.plot(kind='bar' , figsize = (5,3) )
plt.title('Comparison of fradulent and non-fradulant Avg. claims'  )
plt.show()


# ### 16. Is there any similarity in the amount claimed by males and females?

# In[45]:


claim_male = Final_data['claim_amount'].loc[Final_data['gender']=="Male"]
claim_female = Final_data['claim_amount'].loc[Final_data['gender']=="Female"]


# In[46]:


print("The average amount claimed by males is {}".format(claim_male.mean().round(2)))
print("The average amount claimed by females is {}".format(claim_female.mean().round(2)))

print('The average amount claimed by males and females is almost similar')


# ### 17. Is there any relationship between age category and segment?

# In[47]:


#H0 = No Relatipnship
#Ha = tere is a relationship between

#critical : 95%    / significance = 5%



agecat_seg = pd.crosstab(Final_data.AgeGroup, Final_data.Segment, margins = True)
agecat_seg


# In[48]:


stats.chi2_contingency(observed= agecat_seg)


# In[49]:


print('''Value is more than 0.05  So we reject the null ,
therefore there is no relation between age groups and insurance claims ''')


# ### 18. The current year has shown a significant rise in claim amounts as compared to 2016-17 fiscal average which was $10,000.
# 
# 

# In[50]:


Final_data['Year'] = Final_data['claim_date'].dt.year


# In[51]:


Average_2016_17 = Final_data[Final_data['Year'].isin([2016, 2017])]['claim_amount'].mean()


# In[52]:


plt.figure(figsize=(5, 8))
plt.plot(Final_data['Year'], Final_data['claim_amount'] , marker='o', linestyle='-', color='b', label='Claim Amount')
plt.axhline(y=Average_2016_17, color='r', linestyle='--', label='2016-17 Fiscal Average')
plt.legend()
plt.show()


# In[53]:


Final_data['Year'].unique()


# In[54]:


current_year = 2018
average_current_year = Final_data[Final_data['Year'] == current_year]['claim_amount'].mean()

if average_current_year > Average_2016_17:
    print(f"The average claim amount for {current_year} is higher than the 2016-17 fiscal average.")
else:
    print(f"The average claim amount for {current_year} is not significantly higher than the 2016-17 fiscal average.")


# ### 19. Is there any difference between age groups and insurance claims?

# In[64]:


#H0 = No difference between age groups 

Age_group_1 =Final_data['total_policy_claims'].loc[Final_data['AgeGroup']=="Adult"]
Age_group_2 =Final_data['total_policy_claims'].loc[Final_data['AgeGroup']=="Youth"]
Age_group_3 =Final_data['total_policy_claims'].loc[Final_data['AgeGroup']=="Senior"]


# In[66]:


Anova = stats.f_oneway(Age_group_1 , Age_group_2 , Age_group_3 )
Anova


# In[68]:


f = Anova.statistic
p = Anova.pvalue
print("The f-value is {} and the p value is {}".format(f,p))
if(p<0.05):
    print('We reject null hypothesis')
else:
    print('We fail to reject null hypothesis')


# ### 20. Is there any relationship between total number of policy claims and the claimed amount?

# In[55]:


Final_data.total_policy_claims.corr(other= Final_data.claim_amount)


# In[53]:


Final_data


# In[ ]:




