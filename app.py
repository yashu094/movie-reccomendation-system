import streamlit as st
import pickle
import pandas as pd
import requests

similarity = pickle.load(open('similarity.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                            '}?api_key=eb0fa9c183b7d264959a18d37b5eb849&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_poster = []
    recommended_list = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_list.append(movies.iloc[i[0]].title)

    return recommended_list, recommended_movie_poster


movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "How would you like to be contacted",
    movies['title'].values)

if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
