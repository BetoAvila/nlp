import pandas as pd
import numpy as np
import plotly.express as px

# Regex Dictionary
brand = {
    'Coca Cola':
    '.*co[ck][aeo].*|.*sprite.*|.*fanta.*|.*bar[gq].*|.*dr\ p.*|.*pepp.*|.*crush.*|.*sunkist.*|.*canada.*|.*ca.*dry.*|.*pibb*|.*sea.*|.*segr.*|.*fresca.*|.*topo.*|.*7up.*|.*7[\ -]up.*|.*seven\ up.*|.*a\&w.*|.*a\ \&\ w.*|.*stewart.*|.*squirt.*|.*rc.*|.*manza.*|.*maza.*|.*twist.*|.*schwep.*|.*mell.*',
    'Pepsi':
    '.*peps.*|.*pesp.*|.*dew.*|.*code\ red.*|.*live\ wire.*|.*mn.*|.*mt.*|.*moun.*|.*sierra\ mist.*|.*mug.*|.*baja.*|.*baha.*',
    'Novamex': '.*jar[ri].*|.*munde.*',
    'National Beverage': '.*faygo.*',
    'Big Red': '.*big\ r.*',
    'Zevia': '.*zevia.*',
    'AB InBev': '.*stel.*',
    'Hals New York': '.*hal.*',
    'Olipop': '.*olip.*',
    'Modelo': '.*modelo.*',
    'Poppi': '.*poppi.*',
    'Polar Beverages': '.*polar.*',
    'UPTIME Energy': '.*uptime.*|.*up\ time.*',
    'J&R Bottling': '.*brown.*',
    'Bundaberg Brewed Drinks': '.*bundabe.*',
    'Culture Pop Soda': '.*culture.*',
    'Cheerwine': '.*cheerwine.*',
    'Utmost Brands': '.*gus.*|.*grow.*',
    'Boylan Bottling Company': '.*boyl.*',
    'Jones Soda': '.*jones.*'
}

# Reading data
df = pd.read_csv('carbonated_soft_drinks.csv')
df['item'] = df.item_name.str.lower()  # lowercase
df['brand'] = 'UNKNOWN'  # set default brand as UNKNOWN
match = df.item.str.match  # define match call to optimize

# Matching and labeling logic
for k in brand:
    df.brand = np.where(match(brand[k]),
                        np.where(df.brand == 'UNKNOWN', k, df.brand + ',' + k),
                        df.brand)

# Aggregate data to plot
data = df.groupby('brand')\
    .agg({'brand':'count'})\
    .rename({'brand':'count'}, axis=1)\
    .reset_index()\
    .sort_values('count', ascending=False)

# Plot results
fig = px.bar(data,
             x=data.brand,
             y=data['count'],
             color=data.brand,
             title='Brands label')
fig.write_html('report.html')

# Save results to csv file
df[['item_name', 'brand']].to_csv('carbonated_soft_drinks_branded',
                                  index=False)
