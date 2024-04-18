#!/usr/bin/env python
# coding: utf-8

# # Credit Consumption of Customer Case Study

# In[1]:


#Importing libraries 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import scipy.stats as stats


# In[2]:


# Loading datasets

CreditConsumption = pd.read_excel("C:/Analytics/Analytics_T_2.2/CASE_STUDIES/11. Capstone Case Study - Predict Cred Card Consumption/CreditConsumptionData.xlsx")
Cust_Behavior = pd.read_excel("C:/Analytics/Analytics_T_2.2/CASE_STUDIES/11. Capstone Case Study - Predict Cred Card Consumption/CustomerBehaviorData.xlsx")
Cust_Demographics = pd.read_excel("C:/Analytics/Analytics_T_2.2/CASE_STUDIES/11. Capstone Case Study - Predict Cred Card Consumption/CustomerDemographics.xlsx")


# ## EDA(Exploratory Data Analysis)

# ### Checking for data types

# In[3]:


Cust_Behavior.info()


# In[4]:


Cust_Demographics.info()


# In[5]:


Cust_Behavior.isna().sum()


# In[6]:


Cust_Demographics.isna().sum()


# ### Missing Value 

# In[7]:


def Fill_Na(df):
    for column in df.columns:
        if df[column].dtype == 'object':
            df[column].fillna(df[column].mode()[0] , inplace = True)
            
        elif df[column].dtype in ['int64', 'float64']:
            df[column].fillna(df[column].mean(), inplace = True)
            
    return df.isnull().sum()


# In[8]:


Fill_Na(Cust_Behavior)


# In[9]:


Fill_Na(Cust_Demographics)


# In[10]:


# Data Visualization
sns.pairplot(Cust_Demographics)


# In[11]:


#sns.pairplot(Cust_Behavior)


# In[12]:


CreditConsumption.isnull().sum()


# ### Merging the datasets

# In[13]:


Final_data = pd.merge(Cust_Behavior , Cust_Demographics , how = 'inner' , on = 'ID').merge(CreditConsumption, on=  'ID')


# In[14]:


Final_data.rename(columns = {"cc_cons" : "cc_cons_traget"} , inplace= True )


# ### Data cleaning

# In[15]:


# Droping the Loan_eng column as it containg the same values

Final_data.drop(columns='loan_enq' , inplace=True)


# ### Outlier

# In[16]:


#Outlier treatment of the age column
Final_data['age'] = Final_data['age'].clip(lower=Final_data['age'].quantile(0.01), upper=Final_data['age'].quantile(0.95))


# ### Dummy variable 

# In[17]:


#Ordinal catagorical Variable


# In[18]:


Final_data["Income"].value_counts()


# In[19]:


##Dummy column of Income where
# Low = 1
# Medium = 2
# Hing = 3

Final_data["Income"] = pd.Series(np.where(Final_data["Income"]=="Low" , 1 ,  np.where(Final_data["Income"]=="MEDIUM" , 2,3 )))


# In[20]:


Final_data["gender"].value_counts()


# In[21]:


##Dummy column of Gender where
# Male = 1
# Female = 0

Final_data["gender"] = pd.Series(np.where(Final_data["gender"]=="M" , 1 , 0))


# In[22]:


Final_data["account_type"].value_counts()


# In[23]:


##Dummy column of account_type where
# current = 1
# saving = 0

Final_data["account_type"] = pd.Series(np.where(Final_data["account_type"]=="current" , 1 , 0))


# In[24]:


Final_data


# In[25]:


for i in [['region_code' , 'age']]:
    Final_data.loc[:,i]=Final_data[i].astype('category')
    cols = pd.get_dummies(Final_data[i], prefix=i , dtype=int)
    Final_data = pd.concat([Final_data, cols], axis = 1)
    Final_data.drop(i, axis = 1, inplace = True )


# In[27]:


column_names = Final_data.columns.tolist()

# Print column names one by one
for column in column_names:
    print(column)


# ### Data Scaling

# In[28]:


from  sklearn.preprocessing import  StandardScaler


# In[29]:


Sc = StandardScaler()
Sc


# In[30]:


Scaled_data = Sc.fit_transform(Final_data)
Scaled_data


# In[31]:


Scaled_df = pd.DataFrame(Scaled_data , columns=Final_data.columns)


# In[32]:


Scaled_df.isnull().sum().sum()


# In[33]:


data_to_pred = Scaled_df[Scaled_df["cc_cons_traget"].isnull()]


# In[34]:


data_to_process = Scaled_df[~Scaled_df["cc_cons_traget"].isnull()]


# In[35]:


data_to_process.shape


# In[36]:


data_to_process.columns.difference(["cc_cons_traget"])


# In[37]:


from sklearn.model_selection  import train_test_split , cross_val_score  , GridSearchCV , RandomizedSearchCV

X = data_to_process[data_to_process.columns.difference(["cc_cons_traget"])]#with feature columns
y = data_to_process['cc_cons_traget']


# In[38]:


X.shape , y.shape


# In[39]:


#splitting the data in train and test 
X_train, X_test, y_train, y_test  = train_test_split(X,y , test_size=0.3 , random_state=32)


# In[40]:


X_train.shape ,X_test.shape


# In[41]:


from sklearn.neighbors import KNeighborsClassifier , KNeighborsRegressor


# In[42]:


knn_reg = KNeighborsRegressor( n_neighbors=50 , weights='distance')
knn_reg


# In[43]:


Scaled_df.info()


# In[44]:


params = {"n_neighbors":np.random.randint(100, 1000, size=50) ,
    "weights":["uniform", "distance"],
    "metric":["euclidean", "minkowski"]}


# In[45]:


Model = RandomizedSearchCV(estimator=knn_reg, param_distributions=params, cv = 10 ,  scoring='neg_root_mean_squared_error' , random_state=42 )


# In[46]:


Model.fit(X_train , y_train)


# In[47]:


Model.best_score_


# In[48]:


Model.best_params_


# In[56]:


KNN_reg_model = KNeighborsRegressor(weights= 'uniform', n_neighbors= 842, metric= 'euclidean')


# In[57]:


KNN_reg_model.fit(X_train , y_train)


# In[58]:


X_train_preds = KNN_reg_model.predict(X_train)
X_test_preds = KNN_reg_model.predict(X_test)


# In[59]:


def Rmspe(y_true , y_pred):
    
    percentage_error = ((y_true - y_pred)/y_true)*100
    
    # Ignore cases where y_true is zero to avoid division by zero
    percentage_error = percentage_error[y_true != 0]
    
    #calculating square percentage error
    Squared_percentage_error = np.square(percentage_error)
    
    #calculating mean square percentage error
    mean_squared_percentage_error = np.mean(Squared_percentage_error)
    
    #calculating root mean square percentage error(Rmspe)
    Rmspe = np.sqrt(mean_squared_percentage_error)
    
    return Rmspe
    


# In[60]:


Rmspe(y_train  , X_train_preds)


# In[61]:


Rmspe( y_test  , X_test_preds)


# In[62]:


data_to_pred.columns


# In[63]:


data_to_pred.drop(columns='cc_cons_traget',inplace=True)


# In[64]:


data_to_pred.columns


# In[65]:


data_topred = data_to_pred.reindex(sorted(data_to_pred.columns), axis=1)


# In[66]:


#Scaled pred values 
pred_val=pd.Series(KNN_reg_model.predict(data_topred))
pred_val


# In[ ]:




