import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

url = "https://www.imdb.com/search/title/"

query_params ={
    # we insert the search parameters for movies released past five years
    "release_date" : f'{pd.Timestamp.now().year - 5}-01-01, {pd.Timestamp.now().strftime("%Y-%m-%d")}',
    "title_type": "feature",
    "num_votes":"1000,",
    "count":"250"
    }

response = requests.get(url, params=query_params)
html= response.content

soup = bs(html,'html.parser')

#find the containers in the page
containers = soup.find_all('div', {'class':'lister-item mode-advanced'})


data = []

# loop through each container to extract a movie data
for movie in containers:
    
    #exttract the movie title
    title =movie.h3.a.text.strip()
    
    #extract the release year 
    year = movie.h3.find('span',{'class':'lister-item-year'}).text.strip()
    year = year.replace('(','').replace(')','').split()[-1]
    
    #extract the movie duration
    runtime = movie.find('span',{'class':'runtime'}).text.strip()
    
    #extract the genre catgory of the movie
    genre = movie.find('span', {'class': 'genre'}).text.strip()
    
    #extarct the movie rating
    rating = movie.strong.text.strip()
    
    #extract the metascore of the movie
    metascore = movie.find('span', {'class': 'metascore'})
    if metascore is not None:
        metascore = metascore.text.strip()
    else:
        metascore =""
    
    #extract the total votes of the movie
    votes = movie.find('span', {'name':'nv'})['data-value']
    
    #add the data to our empty list movies
    data.append([title,year,runtime,genre,rating, metascore,votes])

#Load the data to dataframe with a rating sort.
df=pd.DataFrame(data, columns=['title','year','runtime','genre','rating', 'metascore','votes']).sort_values("rating", ascending=False)
df.head()
df.info()