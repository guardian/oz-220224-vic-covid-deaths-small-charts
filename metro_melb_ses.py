#%%

import pandas as pd 

fillo = 'input/Vic Covid deaths data - Sheet1.csv'

# testo = "-testo"
testo = ''
chart_key = f"oz-melbourne-deaths-irsad{testo}"

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
tog['LGA'] = tog['LGA'].str.replace(r'\(.+\)', '').str.strip()

tog['IRSAD Quintile']= pd.qcut(tog['IRSAD'], 
                             q = 5, labels = False)

tog['IRSAD Quintile'] = tog['IRSAD Quintile'] + 1

tog.loc[tog["IRSAD Quintile"] == 1, "IRSAD Quintile"] = "Quintile 1 (most disadvantaged)"
tog.loc[tog["IRSAD Quintile"] == 2, "IRSAD Quintile"] = "Quintile 2"
tog.loc[tog["IRSAD Quintile"] == 3, "IRSAD Quintile"] = "Quintile 3"
tog.loc[tog["IRSAD Quintile"] == 4, "IRSAD Quintile"] = "Quintile 4"
tog.loc[tog["IRSAD Quintile"] == 5, "IRSAD Quintile"] = "Quintile 5 (most advantaged)"

metro_melbourne = ['Banyule', 'Bayside', 'Boroondara', 'Brimbank', 'Cardinia', 
'Casey', 'Darebin', 'Frankston', 'Glen Eira', 'Greater Dandenong', 'Hobsons Bay',
'Hume', 'Kingston', 'Knox', 'Manningham', 'Maribyrnong', 'Maroondah', 'Melbourne', 
'Melton', 'Monash', 'Moonee Valley', 'Moreland', 'Mornington Peninsula', 'Nillumbik', 
'Port Phillip', 'Stonnington', 'Whitehorse', 'Whittlesea', 'Wyndham', 'Yarra', 'Yarra Ranges']

lgas = tog['LGA'].unique().tolist()

print("Num in metro melbourne list", len(metro_melbourne))
print("Num of LGAs in our list", len(lgas))

inner = [x for x in metro_melbourne if x in lgas]

print("Num of lgas after I subset", len(inner))

melb = tog.loc[tog['LGA'].isin(metro_melbourne)]
melb = melb.loc[melb['Deceased Cases'] != "< 5"]
melb['Deceased Cases'] = pd.to_numeric(melb['Deceased Cases'])

with open('output/melb_consolidated.csv', 'w') as f:
    melb.to_csv(f, index=False, header=True)


# melb['IRSAD Quintile']= pd.qcut(melb['IRSAD'], 
#                              q = 5, labels = False)

# melb['IRSAD Quintile'] = melb['IRSAD Quintile'] + 1

# melb.loc[melb["IRSAD Quintile"] == 1, "IRSAD Quintile"] = "Quintile 1 (most disadvantaged)"
# melb.loc[melb["IRSAD Quintile"] == 2, "IRSAD Quintile"] = "Quintile 2"
# melb.loc[melb["IRSAD Quintile"] == 3, "IRSAD Quintile"] = "Quintile 3"
# melb.loc[melb["IRSAD Quintile"] == 4, "IRSAD Quintile"] = "Quintile 4"
# melb.loc[melb["IRSAD Quintile"] == 5, "IRSAD Quintile"] = "Quintile 5 (most advantaged)"


grp = melb.groupby(by=['IRSAD Quintile'])["Deceased Cases","Population"].sum().reset_index()

grp['Deaths per 100k'] = round((grp['Deceased Cases'] / grp['Population'])*100000, 2)
grp = grp[['IRSAD Quintile', 'Deaths per 100k']]



final = grp.to_dict(orient='records')

p = grp
# p = melb

print(p)
print(p.columns)


from yachtcharter import yachtCharter
template = [
	{
	"title": "Covid deaths per 100k in Melbourne by socioeconomic status",
	"subtitle": "Showing the number of deaths per 100k population in Melbourne LGAs, grouped by IRSAD quintile",
	"footnote": "",
	"source": "Victoria Health, Australian Bureau of Statistics",
	"margin-left": "20",
	"margin-top": "30",
	"margin-bottom": "20",
	"margin-right": "10"
	}
]

yachtCharter(template=template, 
			data=final,
			chartId=[{"type":"horizontalbar"}],
             options=[{"enableShowMore":"FALSE", "autoSort":"FALSE"}],
			chartName=f"{chart_key}")