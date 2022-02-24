#%%

import pandas as pd 

testo = "-testo"
testo = ''
chart_key = f"oz-victorian-deaths-irsad{testo}"

fillo = 'input/Vic Covid deaths data - Sheet1.csv'

#%%

df = pd.read_csv(fillo, skiprows=15)
# df = df[:8]
df = df[['LGA', 'Deceased Cases']]



irsd = pd.read_excel('input/2033055001 - lga indexes.xls', 
sheet_name='Table 1', skiprows=5)


irsd = irsd[['Unnamed: 1', 'Score.1', 'Unnamed: 10']]
irsd.columns = ['LGA', 'IRSAD', 'Population']
irsd = irsd.dropna(subset=['IRSAD'])



tog = pd.merge(df, irsd, on='LGA', how='left')
tog = tog.loc[~tog['IRSAD'].isna()]

tog['LGA'] = tog['LGA'].str.replace(r'\(.+\)', '').str.strip()

# tog = tog.sort_values(by='Deceased Cases', ascending=False)

tog = tog.sort_values(by='IRSAD', ascending=True)

tog = tog.loc[tog['Deceased Cases'] != "< 5"]

tog['Deceased Cases'] = pd.to_numeric(tog['Deceased Cases'])
tog['Deaths per 100k'] = round((tog['Deceased Cases'] / tog['Population'])*100000, 2)


tog = tog[['LGA', 'Deaths per 100k']]
final = tog.to_dict(orient='records')






p = tog

# p = p.loc[p['IRSAD'].isna()]


print(p)
print(p.columns.tolist())

# #%%

template = [
	{
	"title": "Covid deaths by Local Government Area per 100k population",
	"subtitle": "LGAs ordered by socioeconomic status, from most to least disadvantaged",
	"footnote": "Deaths where the LGA is unknown and LGAs with less than 5 deaths have been excluded",
	"source": "Victoria Health, Australian Bureau of Statistics' SEIFA indexes",
	"margin-left": "20",
	"margin-top": "10",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]

from yachtcharter import yachtCharter
yachtCharter(template=template, 
			data=final,
			chartId=[{"type":"horizontalbar"}],
             options=[{"enableShowMore":"TRUE", "autoSort":"FALSE"}],
			chartName=f"{chart_key}")

# #%%