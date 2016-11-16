import pandas as pd
from pymongo import MongoClient
from sklearn.preprocessing import LabelEncoder


def connect_to_database(database_name):
    client = MongoClient()
    db = client[database_name]
    return db


def convert_collection_to_df(db, collection_name):
    input_data = db[collection_name]
    df = pd.DataFrame(list(input_data.find()))
    return df


def clean_data(df):
    df.drop('_id', axis=1, inplace=True)
    df.drop_duplicates(['state', 'topic', 'user', 'text'])
    df.topic = df.topic.apply(lambda top: top.replace(" (Closed topic)", ""))
    return df


def format_edges(clean):
    df = pd.DataFrame(clean.groupby(['user', 'topic']).count())['text'].reset_index()
    df.rename(columns={'text': 'count'}, inplace=True)


def combining_dataframes(df1, df2):
    new_df = pd.concat([df1, df2])
    return new_df
