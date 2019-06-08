import pandas
import wikipedia as wp
from bs4 import BeautifulSoup
html = wp.page("List of postal codes of Canada: M").html().encode("UTF-8")
dataframe = pandas.read_html(html, header = 0)[0]
dataframe = dataframe[dataframe.Borough != 'Not assigned']
dataframe = dataframe.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(list).apply(lambda x:', '.join(x)).to_frame().reset_index()
for index, row in dataframe.iterrows():
    if row['Neighbourhood'] == 'Not assigned':
        row['Neighbourhood'] = row['Borough']

print(dataframe)
print(dataframe.shape)