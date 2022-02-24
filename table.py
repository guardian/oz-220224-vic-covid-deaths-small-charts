#%%

import pandas as pd 

testo = "-testo"
testo = ''
chart_key = f"oz-victorian-deaths-irsad-table{testo}"

# fillo = 'input/Vic Covid deaths data - Sheet1.csv'
fillo = 'input/Vic Covid deaths data - Sheet2.csv'

#%%

df = pd.read_csv(fillo)
# df = df[:8]
df = df[['LGA', 'Deceased Cases']]
df.columns = ['LGA', 'Deaths']
df['LGA'] = df['LGA'].str.replace(r'\(.+\)', '').str.strip()
df = df.loc[~df['LGA'].isin(['Total Cases', 'Unknown', 'Overseas', 'Interstate'])]
print(df)

final = df.to_dict(orient='records')

from yachtcharter import yachtCharter
template = [
	{
	"title": "Covid deaths by LGA",
	"subtitle": "Showing the number of deaths during the Omicron wave by LGA",
	"footnote": "",
	"source": "Victoria Health",
	"margin-left": "20",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]

yachtCharter(template=template, 
            options=[{"colorScheme":"guardian","format": "scrolling",
            "enableSearch": "TRUE","enableSort": "FALSE"}],
			data=final,
			chartId=[{"type":"table"}],
			chartName=f"{chart_key}")

# # #%%