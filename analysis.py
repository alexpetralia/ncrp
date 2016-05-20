import os
import pandas as pd

from dictionary import DATA_DICTIONARY

def df_return_pct(df):
    value_counts = df.groupby('ADMTYPE')['SENTLGTH'].value_counts().reset_index().rename(columns={0: 'Count'})
    total = df.groupby('ADMTYPE').count().reset_index()[['ADMTYPE', 'RACE']]
    df = value_counts.merge(total, on='ADMTYPE')
    df['Percent'] = df['Count'] / df['RACE']
    df = df.rename(columns={'RACE': 'Total'})
    return df

if __name__ == '__main__':
    
    ROOT = os.path.dirname(__file__)
    
    # Read in data
    a = pd.read_table(os.path.join(ROOT, 'data_admissions.tsv'), sep='\t', nrows=100000)
    r = pd.read_table(os.path.join(ROOT, 'data_releases.tsv'), sep='\t', nrows=100000)
    p = pd.read_table(os.path.join(ROOT, 'data_yr_end_population.tsv'), sep='\t', nrows=100000)
    
    # Recode variables
    [df[col].replace(DATA_DICTIONARY[col], inplace=True) for df in [a, r, p] for col in df.columns]
    
    ############
    # ANALYSIS #
    ############    
    
    # Offense by race (only most serious offense is listed - there can be multiple)
    b = a[ (a['RACE'] == 'Black, non-Hispanic') & (a['OFFGENERAL'] == 'Drugs')]
    b = df_return_pct(b) # 40% get over 5 years   
    
    h = a[ (a['RACE'] == 'Hispanic, any race') & (a['OFFGENERAL'] == 'Drugs')]
    h = df_return_pct(h) # 42% get over 5 years   
    
    w = a[ (a['RACE'] == 'White, non-Hispanic') & (a['OFFGENERAL'] == 'Drugs')]
    w = df_return_pct(w) # 34% get over 5 years   
    
    
    
