import pandas as pd
import numpy as np
import sqlalchemy as sq
from .config import DevelopmentConfig
from sklearn.metrics.pairwise import cosine_similarity 

#Import Data
engine = sq.create_engine(DevelopmentConfig.SQLALCHEMY_DATABASE_URI)

def film_data():
    film_data = pd.read_sql_table("film",engine)
    film_data.drop(['image_name'],axis=1, inplace=True)
    return film_data

def rating_data():
    rating_data = pd.read_sql_table("ratings",engine)
    rating_data.drop(['id'],axis=1, inplace=True)
    rating_data.sort_values(by=['film_id'], inplace = True)
    rating_data.rename(columns={"film_id":"id"}, inplace=True)
    return rating_data

def merge_data():
    data = pd.merge(left=film_data(), right=rating_data(), how='left', left_on='id',right_on='id')
    data.fillna(0,inplace=True)
    return data

def standardize(row):
    new_row = (row - row.mean())/(row.max()-row.min())
    return new_row

def matrix_data():
    #row_index = data[data['user_id'] > 0]['user_id'].unique()
    rating = merge_data()[['rating']].apply(standardize)
    df = merge_data()[['user_id','title']]
    df['rating'] = rating
    matrix_data = df.pivot_table(values='rating',index='user_id',columns='title').fillna(0)
    return matrix_data

def get_similarity_scores():
    similarity_scores = cosine_similarity(matrix_data().T)
    return similarity_scores

def get_item_similarity_df():
    item_similarity_df = pd.DataFrame(get_similarity_scores(),index=matrix_data().columns,columns=matrix_data().columns)
    return item_similarity_df

def get_similar_films(film_name, user_rating):
    similar_score = get_item_similarity_df()[film_name]*user_rating
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score

def recommended_model(action_lover):
    #action_lover = [("2012",2),("Fast and Furious 8",3)]
    similar_films = pd.DataFrame()

    for film,rating in action_lover:
        similar_films = similar_films.append(get_similar_films(film,rating),ignore_index=True)
    
    recommended_film = similar_films.sum().sort_values(ascending=False)
    for film,rating in action_lover:
        recommended_film.pop(film)

    return recommended_film.index