import streamlit as st 
import pandas as pd 
import matplotlib.pyplot as plt
import plotly.express as px 

movie_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")

movie_data.info()

movie_data.duplicated()

movie_data.count()

movie_data.dropna()

st.write("""
Average Movie Budget, Grouped by Genre
""")

avg_budget = movie_data.groupby("genre")["budget"].mean().round()
avg_budget = avg_budget.reset_index()
genre = avg_budget["genre"]
avg_bud = avg_budget["budget"]


fig = plt.figure(figsize = (20, 5))
plt.bar(genre, avg_bud, color = "blue")
plt.xlabel("Genre")
plt.ylabel("Average Movie Budget")
plt.title("Average Movie Budget, Grouped by Genre")

st.pyplot(fig)


score_rating =  movie_data['score'].unique().tolist()
genre_list =  movie_data['genre'].unique().tolist()
year_list =  movie_data['year'].unique().tolist()


with st.sidebar:
    st.write("Select a range on the slider (it represents movie score) \
       to view the total number of movies in a genre that falls \
       within that range ")
    
    new_score_rating = st.slider(label = "Score Rating", min_value=1.0, max_value=10.0, value=(3.0,4.0))
    new_genre_list = st.multiselect(label = "Genre", options = genre_list,  default = genre_list)
    year = st.selectbox('Choose a Year', year_list, 0)

    score_info = (movie_data['score'].between(*new_score_rating))
    new_genre_year = (movie_data['genre'].isin(new_genre_list)) \
    & (movie_data['year'] == year)


col1, col2 = st.columns([2,3])
with col1:
    st.write("""#### Lists of movies filtered by year and Genre """)
    dataframe_genre_year = movie_data[new_genre_year]
    st.dataframe(dataframe_genre_year, width=400)

with col2:
    st.write("""#### User score of movies and their genre """)
    rating_count_year = movie_data[score_info]\
    .groupby('genre')['score'].count()
    rating_count_year = rating_count_year.reset_index()
    figpx = px.line(rating_count_year, x = 'genre', y = 'score')
    st.plotly_chart(figpx)
