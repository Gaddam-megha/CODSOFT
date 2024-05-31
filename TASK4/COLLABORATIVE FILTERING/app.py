import os
import pickle
import streamlit as st
import numpy as np


st.header('Book Recommender System Using Machine Learning')

# Define file paths
model_path = 'artifacts/model.pkl'
books_name_path = 'artifacts/books_name.pkl'
final_rating_path = 'artifacts/final_rating.pkl'
book_pivot_path = 'artifacts/book_pivot.pkl'

# Function to load pickle files safely
def load_pickle(file_path):
    try:
        with open(file_path, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error(f"FileNotFoundError: The file '{file_path}' was not found.")
        st.stop()  # Stop execution if a file is not found
    except Exception as e:
        st.error(f"An error occurred while loading '{file_path}': {e}")
        st.stop()  # Stop execution +++if any other error occurs

# Load the necessary files
model = load_pickle(model_path)
book_names = load_pickle(books_name_path)
final_rating = load_pickle(final_rating_path)
book_pivot = load_pickle(book_pivot_path)

def fetch_poster(suggestion):
    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion:
        book_name.append(book_pivot.index[book_id])

    for name in book_name[0]:
        try:
            ids = np.where(final_rating['title'] == name)[0][0]
            ids_index.append(ids)
        except IndexError:
            st.error(f"Error: The book '{name}' was not found in the final_rating DataFrame.")
            continue

    for idx in ids_index:
        try:
            if 'img-url' in final_rating.columns:
                url = final_rating.iloc[idx]['img-url']
                poster_url.append(url)
            else:
                st.error("The key 'img-url' does not exist in the final_rating DataFrame.")
                st.stop()
        except IndexError:
            st.error(f"Error: Invalid index '{idx}' for final_rating DataFrame.")
            continue

    return poster_url

def recommend_book(book_name):
    books_list = []
    try:
        book_id = np.where(book_pivot.index == book_name)[0][0]
    except IndexError:
        st.error(f"Error: The book '{book_name}' was not found in the book_pivot DataFrame.")
        return [], []

    distance, suggestion = model.kneighbors(book_pivot.iloc[book_id, :].values.reshape(1, -1), n_neighbors=6)

    poster_url = fetch_poster(suggestion)

    for i in range(len(suggestion)):
        books = book_pivot.index[suggestion[i]]
        for j in books:
            books_list.append(j)
    return books_list, poster_url

selected_books = st.selectbox(
    "Type or select a book",
    book_names
)

if st.button('Show Recommendation'):
    recommended_books, poster_url = recommend_book(selected_books)
    if recommended_books and poster_url:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(recommended_books[1])
            st.image(poster_url[1])
        with col2:
            st.text(recommended_books[2])
            st.image(poster_url[2])
        with col3:
            st.text(recommended_books[3])
            st.image(poster_url[3])
        with col4:
            st.text(recommended_books[4])
            st.image(poster_url[4])
        with col5:
            st.text(recommended_books[5])
            st.image(poster_url[5])