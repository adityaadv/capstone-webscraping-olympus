from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests
from time import sleep
from random import randint

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
pages = range(1,250,50)
movie_data = [] # initiating tuple

for page in pages:
    page = requests.get("https://www.imdb.com/search/title/?release_date=2019-01-01,2019-12-31&start="+str(page)+"&ref_=adv_nxt")
    soup = BeautifulSoup(page.text, 'html.parser')
    items = soup.find_all('div', attrs = {'class':'lister-item mode-advanced'})
    sleep(randint(2, 8))
    # initiating scrapping process
    for it in items:
        title = it.find('img')['alt']
        rating = it.find('div', attrs={'class':'inline-block ratings-imdb-rating'})['data-value']
        try : score = it.find('span', attrs={'class':'metascore favorable'}).text.replace('        ','')
        except : score = 0
        vote = it.find('span', attrs={'name':'nv'})['data-value']
        movie_data.append([title, rating, score, vote])

#change into dataframe
movie_df = pd.DataFrame(movie_data, columns = ('title', 'imdb_rating', 'metascore','vote'))

#insert data wrangling here
movie_df['title'] = movie_df['title'].astype('object')
movie_df['imdb_rating'] = movie_df['imdb_rating'].astype('float')
movie_df[['metascore', 'vote']] = movie_df[['metascore', 'vote']].astype('int') 

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'IMDB Rates: {movie_df["imdb_rating"].mean().round(2)}'

	# generate plot
	ax = movie_df['imdb_rating'].plot(kind='hist', figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# generate plot
	ax2 = movie_df['vote'].plot(kind='hist', figsize = (20,9))
	
	# Rendering plot
	# Do not change this
	figfile2 = BytesIO()
	plt.savefig(figfile2, format='png', transparent=True)
	figfile2.seek(0)
	figdata2_png = base64.b64encode(figfile2.getvalue())
	plot2_result = str(figdata2_png)[2:-1]
	
	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result,
		plot2_result=plot2_result
		)


if __name__ == "__main__": 
    app.run(debug=True)
