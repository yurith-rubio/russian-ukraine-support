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

# I need to make a table with the data from the support.csv file and the color that each country will have in the map.

# Afganistan - NEUTRAL - #FFF