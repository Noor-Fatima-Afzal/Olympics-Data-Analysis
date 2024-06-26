import pandas as pd

def preprocess(df, df_region):
    # filtering for summar olymics
    df = df[df['Season']=='Summer']
    # merge with region dataframe 
    df = df.merge(df_region, on='NOC', how='left')
    # droppring duplicates
    df.drop_duplicates(inplace=True)
    # one hot encoding medals and concatenating with original dataframe
    df = pd.concat( [df, pd.get_dummies(df['Medal'])], axis=1)
    return df