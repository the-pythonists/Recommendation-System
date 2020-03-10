'''
Main Script used for Recommendation System
'''


import pandas as pd
import numpy as np

# importing our Videos Table from models 
# and then creating dataframe 
from App.models import Videos_Data
from django_pandas.io import read_frame


query = Videos_Data.objects.all()
df = read_frame(query)


df['Description'].head()

from sklearn.feature_extraction.text import TfidfVectorizer

tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

df['Description'] = df['Description'].fillna('')


tfv_matrix = tfv.fit_transform(df['Description'])


from sklearn.metrics.pairwise import sigmoid_kernel

sig = sigmoid_kernel(tfv_matrix,tfv_matrix)


indices = pd.Series(df.index,index = df['Title']).drop_duplicates()


indices.head()


def recommender(title, sig=sig):
    idx = indices[title]
    
    sig_scores = list(enumerate(sig[idx]))
    
    sig_scores = sorted(sig_scores,key=lambda x:x[1],reverse=True)
    
    sig_scores = sig_scores[1:11]
    
    movie_indices = [i[0] for i in sig_scores]
    
    return df['Title'].iloc[movie_indices]
