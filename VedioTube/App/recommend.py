#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from App.models import Videos_Data
from django_pandas.io import read_frame
# In[4]:


query = Videos_Data.objects.all()
df = read_frame(query)

# df = pd.read_csv('C:\\repos\\Recommendation-System\\VideoPlayer\\App\\VideoData.csv')


# In[6]:


# df.head()


# In[7]:


df['Description'].head()


# In[10]:


from sklearn.feature_extraction.text import TfidfVectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

df['Description'] = df['Description'].fillna('')


# In[11]:


tfv_matrix = tfv.fit_transform(df['Description'])


# In[12]:


tfv_matrix.shape


# In[13]:


from sklearn.metrics.pairwise import sigmoid_kernel

sig = sigmoid_kernel(tfv_matrix,tfv_matrix)


# In[14]:


indices = pd.Series(df.index,index = df['Title']).drop_duplicates()


# In[15]:


indices.head()


# In[18]:


def recommender(title, sig=sig):
    idx = indices[title]
    
    sig_scores = list(enumerate(sig[idx]))
    
    sig_scores = sorted(sig_scores,key=lambda x:x[1],reverse=True)
    
    sig_scores = sig_scores[1:11]
    
    movie_indices = [i[0] for i in sig_scores]
    
    return df['Title'].iloc[movie_indices]


# In[19]:


# recommender('AndhaDhun - Official Trailer  Tabu  Ayushmann Khurrana  Radhika Apte  5th October')


# In[ ]:




