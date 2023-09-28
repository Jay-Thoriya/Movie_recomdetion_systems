import streamlit as st 
import pickle 
import pandas as pd
import requests
import streamlit as st
from PIL import Image
import base64



def fetch_poster (movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=e80cc8d7e60a11ec8cc264c8038633ec&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)),reverse= True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch Poster from API 
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))


background_image_url = "https://wpassets.brainstation.io/app/uploads/2017/04/13100509/Netflix-Background.jpg"

# Use CSS to set the background image
st.markdown(
    f"""
    <style>
        .stApp {{
            background-image: url("{background_image_url}");
            background-size: cover;
        }}
    </style>
    """,
    unsafe_allow_html=True
)
# Inject custom CSS for the specific class
custom_css = """
<style>
.st-emotion-cache-1n76uvr.e1f1d6gn0 {
    background-color: black ;
    /* From https://css.glass */
    background: rgba(5, 0, 0, 0) !important;
    border-radius: 16px !important;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
    backdrop-filter: blur(4.9px) !important;
    -webkit-backdrop-filter: blur(4.6px) !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
    padding: 33px !important;
    box-shadow: rgba(0, 0, 0, 0.25) 0px 54px 55px, rgba(0, 0, 0, 0.12) 0px -12px 30px, rgba(0, 0, 0, 0.12) 0px 4px 6px, rgba(0, 0, 0, 0.17) 0px 12px 13px, rgba(0, 0, 0, 0.09) 0px -3px 5px !important;
}
.st-b8{
    width: 85% !important;
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

st.title(":red[Movie Recommender System] ")

selected_movie_name = st.selectbox(
    "Enter a movie title, and we'll suggest similar films for you",
    movies['title'].values)  

if st.button('Recommend'):
    name,poster = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3]) 
        st.image(poster[3])

    with col5:
        st.text(name[4])
        st.image(poster[4])


##