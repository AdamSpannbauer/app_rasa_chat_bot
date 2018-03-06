import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

#set up urls of interest
chart_base_url = 'https://www.apple.com/itunes/charts/'
#top 100 chart url exts
charts = ['top-grossing-apps','paid-apps','free-apps']

chart_data = []
#iterate over chart names
for chart in charts:
	print('gathering data for {}'.format(chart))
	#build url of interest
	url = chart_base_url + chart

	#scrape html
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html5lib")

	#create list for app rank
	app_ranks = range(1,101)
	#extract app names from html
	app_names = [x.text for x in soup.select('h3 a')]
	#extract app genre from html
	app_genre = [x.text for x in soup.select('h4 a')]
	
	#create df from app data
	chart_df = pd.DataFrame(
		{'rank': app_ranks, 
		 'name': app_names, 
		 'genre': app_genre}
		 )
	#create column for chart name
	chart_df['chart'] = chart
	#append df to chart data list
	chart_data.append(chart_df)

#rbind all dfs
full_chart_data = pd.concat(chart_data, ignore_index=True)

#write out to csv
full_chart_data.to_csv('data/app_chart_data.csv', encoding='utf-8')
