import sqlite3
import json

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

conn = sqlite3.connect('../../krisha.kz/db.sqlite')
query = """
SELECT * FROM flats
JOIN prices ON flats.id = prices.flat_id
"""

df = pd.read_sql_query(query, conn)
conn.close()

df['specs'] = df['specs'].apply(json.loads)

# 2. Flatten the 'specs' column into a new DataFrame
specs_expanded = pd.json_normalize(df['specs'])

# 3. Join the new columns back to your original DataFrame
df = pd.concat([df.drop('specs', axis=1), specs_expanded], axis=1)
df.drop(columns=['id', 'url', 'photo', 'flat_id', 'star'], inplace=True)
df = df.rename(columns={'type': 'internet', 'balcony_g': 'balcony_glazing'})

print(df.columns.tolist())
# print(df.dtypes)
print(df.nunique())

# booleans: priv_dorm, furniture, has_change, balcony_glazing