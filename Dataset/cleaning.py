#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)


# In[5]:


df = pd.read_csv('C:/Users/shubh/OneDrive/Desktop/Projects/Chat_Bot/Dataset/College_data.csv')


# In[7]:


df_clean = df.copy()


# In[9]:


df_clean.head()


# In[11]:


df_clean.info()


# In[13]:


df_clean.describe()


# In[15]:


df_clean.dtypes


# In[17]:


df_clean['UG_fee'] = pd.to_numeric(df['UG_fee'], errors='coerce')
df_clean['PG_fee'] = pd.to_numeric(df['PG_fee'], errors='coerce')
df_clean['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')


# In[19]:


df_clean.dtypes


# In[21]:


df_clean.describe()


# In[23]:


df_clean.isnull().sum()


# In[25]:


for col in ['Academic', 'Accommodation', 'Faculty', 'Infrastructure', 'Placement', 'Social_Life']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')


# In[27]:


df_clean.isnull().sum()


# In[38]:


//need editing and understading
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(10,5))
sns.barplot(x=df.columns,y=df.isnull().sum()/len(df))
plt.xticks(rotation=90) # if the graph is big than rotation not required
plt.show()


# In[42]:


//need editing and understanding
df_plot = df.groupby(by=['State']).College_Name.nunique()
plt.figure(figsize=(20,7))
plt.xticks(rotation=90)
sns.barplot(x=df_plot.index,y=df_plot)


# In[29]:


df_clean.info()


# In[31]:


df_clean.isnull().sum()


# In[43]:


df_clean['UG_fee'] = df_clean['UG_fee'].replace(['--', 'NAN', 'Not Available', '', 'NA'], np.nan)


# In[33]:


# Common invalid placeholders
invalid_values = ['--', 'NAN', 'Not Available', '', 'NA']

df_clean['Faculty']   = df_clean['Faculty'].replace(invalid_values, np.nan)	
df_clean['PG_fee']    = df_clean['PG_fee'].replace(invalid_values, np.nan)
df_clean['Placement'] = df_clean['Placement'].replace(invalid_values, np.nan)
df_clean['Rating']    = df_clean['Rating'].replace(invalid_values, np.nan)
df_clean['Social_Life']    = df_clean['Social_Life'].replace(invalid_values, np.nan)
df_clean['Accommodation'] = df_clean['Accommodation'].replace(invalid_values, np.nan)
df_clean['Academic']  = df_clean['Academic'].replace(invalid_values, np.nan)
df_clean['Infrastructure']    = df_clean['Infrastructure'].replace(invalid_values, np.nan)


# In[35]:


df_clean.isnull().sum()


# In[37]:


df_clean['UG_fee'] = df_clean['UG_fee'].fillna(df_clean['UG_fee'].min())


# In[39]:


# Get all numeric columns except 'UG_fee'
numeric_cols = df_clean.select_dtypes(include='number').columns.drop('UG_fee')

# Fill NaN in these columns with their mean
df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())


# In[41]:


df_clean.isnull().sum()


# In[52]:


df.to_csv("C:/Users/shubh/OneDrive/Desktop/Projects/Chat_Bot/Dataset/cleaned_college_data.csv", index=False)


# In[43]:


def get_colleges(df, State=None, max_fee=None, min_placement=None, course=None, top_n=10):
    df_filtered = df.copy()  # Work on a copy so original stays safe

    # 1. Filter by State (case-insensitive match)
    if State:
        df_filtered = df_filtered[
            df_filtered['State'].notnull() & 
            (df_filtered['State'].str.lower() == State.lower())
        ]

    # 2. Filter by UG_fee if provided
    if max_fee:
        df_filtered = df_filtered[
            df_filtered['UG_fee'].notnull() & (df_filtered['UG_fee'] <= max_fee)
        ]

    # 3. Filter by Placement if provided
    if min_placement:
        df_filtered = df_filtered[
            df_filtered['Placement'].notnull() & (df_filtered['Placement'] >= min_placement)
        ]

    # 4. Filter by Stream/Course (partial match, case-insensitive)
    if course:
        df_filtered = df_filtered[
            df_filtered['Stream'].notnull() & 
            df_filtered['Stream'].str.lower().str.contains(course.lower(), na=False)
        ]

    # 5. Return top_n colleges sorted by Placement (descending)
    return df_filtered[
        ['College_Name', 'State', 'UG_fee', 'Placement', 'Rating']
    ].sort_values(by='Placement', ascending=False).head(top_n)


# In[45]:


get_colleges(df_clean, State="Maharashtra", max_fee=500000, min_placement=60, course="Engineering")


# In[47]:


get_colleges(df_clean, State="Delhi")


# In[49]:


get_colleges(df_clean, State="Maharashtra")


# In[53]:


get_colleges(df_clean, State="Maharashtra", max_fee=500)


# In[61]:


get_colleges(df_clean, State="Maharashtra", max_fee=500000, min_placement=60)


# In[57]:


get_colleges(df_clean, State="Maharashtra", course="Engineering")


# In[ ]:




