import pandas
import wikipedia as wp
from bs4 import BeautifulSoup
import requests 
import io
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
html = wp.page("List of postal codes of Canada: M").html().encode("UTF-8")
dataframe = pandas.read_html(html, header = 0)[0]
dataframe = dataframe[dataframe.Borough != 'Not assigned']
dataframe = dataframe.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(list).apply(lambda x:', '.join(x)).to_frame().reset_index()
for index, row in dataframe.iterrows():
    if row['Neighbourhood'] == 'Not assigned':
        row['Neighbourhood'] = row['Borough']

url="http://cocl.us/Geospatial_data"
s=requests.get(url).content
c=pandas.read_csv(io.StringIO(s.decode('utf-8')))
c.columns = ['Postcode', 'Latitude', 'Longitude']
dataframe = pandas.merge(c, dataframe, on='Postcode')
dataframe = dataframe[['Postcode', 'Borough', 'Neighbourhood', 'Latitude', 'Longitude']]
dataframe['Coordinates'] = list(zip(dataframe.Longitude, dataframe.Latitude))
dataframe['Coordinates'] = dataframe['Coordinates'].apply(Point)
gdf = gpd.GeoDataFrame(dataframe, geometry='Coordinates')
cities = gpd.read_file(gpd.datasets.get_path('naturalearth_cities'))
ax = cities[cities.name == "Toronto"].plot(color='white', edgecolor='black')
gdf.plot(ax=ax, color='red')
plt.show()
print(dataframe)