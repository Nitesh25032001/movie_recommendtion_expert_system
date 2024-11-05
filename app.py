import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=7c9bb2704aabef3a581d247607179d95&language=en-US',
            timeout=5  # Set a timeout for the request
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        poster_path = data.get('poster_path')

        # Check if poster_path is available
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            # Placeholder image URL if poster_path is not available
            return "https://via.placeholder.com/500x750.png?text=No+Image+Available"

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return "https://via.placeholder.com/500x750.png?text=Error+Loading+Image"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from api
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('PREDICTORY')

selected_movie_name = st.selectbox(
    "Can't decide on what to watch? Elevate your movie nights with expert picks. This is where every film watching journey begins.",
    movies['title'].values
)

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
