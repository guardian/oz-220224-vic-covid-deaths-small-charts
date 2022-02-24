#%%

import pandas as pd 

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
# 'LGA', 'Deceased Cases', 'LGA_id'

# tog = tog[['LGA_id', 'LGA', 'Deceased Cases']]


tog = tog.loc[tog['Deceased Cases'] != "< 5"]

tog['Deceased Cases'] = pd.to_numeric(tog['Deceased Cases'])
tog['Deaths per 100k'] = round((tog['Deceased Cases'] / tog['Population'])*100000, 2)


tog = tog[['LGA_id','LGA', 'Deaths per 100k']]
tog = tog.dropna(subset=['LGA_id'])

with open('output/chloro.csv', 'w') as f:
    tog.to_csv(f, index=False, header=True)

p = tog

print(p)
print(p.columns)