import pandas as pd
import numpy as np
import json

df = pd.read_csv("data/support.csv")
df = df.rename(columns={'response to russia': 'support'})

df['support'].replace('', np.nan, inplace=True)
df['support'].replace('\u200b', np.nan, inplace=True)

# df.dropna(subset=['support'], inplace=True)

# replace nan with empty string
# using replace() function
df = df.replace(np.nan, 'nan')

dict = df.set_index('country')['support'].to_dict()

# Convert the dict into a json file
dict = json.dumps(dict)

with open('src/lib/support.json', 'w') as f:
    f.write(dict)

df_spendings = pd.read_csv("data/total_spendings.csv")

print(df_spendings) 
# combined_russia = list(zip(df_spendings['russia'], df_spendings['gdp_russia']))
# combined_ukraine = list(zip(df_spendings['ukraine'], df_spendings['gdp_ukraine']))


# df_spendings['russia'] = combined_russia
# df_spendings['ukraine'] = combined_ukraine

# del df_spendings['gdp_russia']
# del df_spendings['gdp_ukraine']

# dict_spendings = df_spendings.set_index('year').to_dict()
# dict_spendings = json.dumps(dict_spendings)

df_spendings.to_json('src/lib/spendings.json', orient='records')

# df_spendings.to_csv('src/lib/spendings.csv', index=False)

# I need to make a table with the data from the support.csv file and the color that each country will have in the map.

# Afganistan - NEUTRAL - #FFF