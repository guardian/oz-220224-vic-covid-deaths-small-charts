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


tog['IRSAD Quintile']= pd.qcut(tog['IRSAD'], 
                             q = 5, labels = False)

tog['IRSAD Quintile'] = tog['IRSAD Quintile'] + 1

tog.loc[tog["IRSAD Quintile"] == 1, "IRSAD Quintile"] = "Quartile 1 (most disadvantaged)"
tog.loc[tog["IRSAD Quintile"] == 2, "IRSAD Quintile"] = "Quartile 2"
tog.loc[tog["IRSAD Quintile"] == 3, "IRSAD Quintile"] = "Quartile 3"
tog.loc[tog["IRSAD Quintile"] == 4, "IRSAD Quintile"] = "Quartile 4"
tog.loc[tog["IRSAD Quintile"] == 5, "IRSAD Quintile"] = "Quartile 5 (most advantaged)"



# 'LGA', 'Deceased Cases', 'LGA_id'

# tog = tog[['LGA_id', 'LGA', 'Deceased Cases']]


tog = tog.loc[tog['Deceased Cases'] == "< 5"]

# tog['Deceased Cases'] = pd.to_numeric(tog['Deceased Cases'])
# tog['Deaths per 100k'] = round((tog['Deceased Cases'] / tog['Population'])*100000, 2)


# tog = tog[['LGA_id','LGA', 'Deaths per 100k']]
tog = tog.dropna(subset=['LGA_id'])

p = tog

# p = p.loc[p['IRSAD'].isna()]


print(p)
print(p.columns.tolist())