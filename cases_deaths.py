#%%
import pandas as pd
import os
import datetime
import pytz
# from modules.syncData import syncData
pd.set_option("display.max_rows", 100)

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
# import fuzzywuzzy

def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
    s = df_2[key2].tolist()
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))
    df_1['matches'] = m
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2

    return df_1

fillo = 'input/Vic Covid deaths data - Sheet1.csv'

#%%

df = pd.read_csv(fillo, skiprows=15)
# df = df[:8]
df = df[['LGA', 'Deceased Cases']]

irsd = pd.read_excel('input/2033055001 - lga indexes.xls', 
sheet_name='Table 1', skiprows=5)


irsd = irsd[['Unnamed: 0','Unnamed: 1', 'Score.1', 'Unnamed: 10']]
irsd.columns = ['LGA_id', 'LGA', 'IRSAD', 'Population']
irsd = irsd.dropna(subset=['LGA'])



tog = pd.merge(df, irsd, on='LGA', how='left')


tog['IRSAD Quintile']= pd.qcut(tog['IRSAD'], 
                             q = 5, labels = False)

tog['IRSAD Quintile'] = tog['IRSAD Quintile'] + 1

tog.loc[tog["IRSAD Quintile"] == 1, "IRSAD Quintile"] = "Quintile 1 (most disadvantaged)"
tog.loc[tog["IRSAD Quintile"] == 2, "IRSAD Quintile"] = "Quintile 2"
tog.loc[tog["IRSAD Quintile"] == 3, "IRSAD Quintile"] = "Quintile 3"
tog.loc[tog["IRSAD Quintile"] == 4, "IRSAD Quintile"] = "Quintile 4"
tog.loc[tog["IRSAD Quintile"] == 5, "IRSAD Quintile"] = "Quintile 5 (most advantaged)"

### Add the cases

cases = pd.read_csv('output/cases.csv')
# 'LGA', 'Cases'

combo = pd.merge(tog, cases, on='LGA', how='left')
# 'LGA', 'Deceased Cases', 'LGA_id', 'IRSAD', 'Population', 'IRSAD Quintile', 'Cases'

combo.dropna(subset=['LGA'], inplace=True)
combo.dropna(subset=['Deceased Cases'], inplace=True)

combo = combo[['LGA', 'Deceased Cases', 'Cases', 'Population', 'IRSAD','IRSAD Quintile']]
combo.columns = ['LGA', 'Deaths', 'Cases', 'Population', 'IRSAD','IRSAD Quintile']

combo = combo.loc[~combo['LGA'].isin(['Total Cases', 'Unknown', 'Overseas', 'Interstate'])]

# with open("output/consolidated.csv", 'w') as f:
#     combo.to_csv(f, index=False, header=True)


p = combo

print(p)
print(p.columns.tolist())


### Initial cases download:


# vic_init = pd.read_csv('https://www.dhhs.vic.gov.au/ncov-covid-cases-by-lga-source-csv')
# # vic_init = pd.read_csv('https://www.coronavirus.vic.gov.au/sites/default/files/2022-01/NCOV_COVID_Cases_by_LGA_Source_20220109.csv')
# vic_max_date = vic_init['diagnosis_date'].max()
# # vic_max_date = vic_max_date.strftime("%Y-%m-%d")
# # %%

# print(vic_init)
# print(vic_init.columns)


# vic = vic_init.copy()
# vic = vic[['diagnosis_date', 'Localgovernmentarea']]
# vic.columns = ['Date', 'LGA']

# vic['Cases'] = 1

# vic = vic.groupby(by=['LGA'])['Cases'].sum().reset_index()

# with open('output/cases.csv', 'w') as f:
#     vic.to_csv(f, index=False, header=True)

# p = vic 

# print(p)
# print(p.columns)

