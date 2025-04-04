import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt

def get_recommendations(selected_genres, num_recommendations, csv_path="data/movies.csv"):
    """
    Generates a dictionary of movie recommendations with actual ratings based on selected genres.

    Args:
        selected_genres (list): A list of genres to filter movies by.
        num_recommendations (int): The number of recommendations to return.
        csv_path (str, optional): The file path of the CSV containing movie data. Defaults to "data/movies.csv".

    Returns:
        dict: A dictionary where keys are movie titles and values are their ratings.

    Raises:
        ValueError: If the CSV file does not contain the required 'Genre', 'Movie', and 'Rating' columns.
    """
    df = pd.read_csv(csv_path)

    if not all(col in df.columns for col in ["Genre", "Movie", "Rating"]):
        raise ValueError("CSV file must contain 'Genre', 'Movie', and 'Rating' columns.")

    recommendations = {}

    for genre in selected_genres:
        genre_movies = df[df["Genre"] == genre][["Movie", "Rating"]].values
        for movie, rating in genre_movies:
            recommendations[movie] = rating
    
    sorted_recommendations = dict(sorted(recommendations.items(), key=lambda item: item[1], reverse=True))
    return dict(list(sorted_recommendations.items())[:num_recommendations])

def plot_scores(recommendations):
    """
    Plots a horizontal bar chart of the recommended movies and their scores.

    The x-axis represents the scores and the y-axis represents the movie titles.
    The chart is sorted in descending order of the scores.

    Args:
        recommendations (dict): A dictionary where keys are movie titles and values are their scores.
    """
    df = pd.DataFrame(list(recommendations.items()), columns=["Movie", "Score"])
    df = df.sort_values(by="Score", ascending=False)
    
    fig, ax = plt.subplots()
    ax.barh(df["Movie"], df["Score"], color='skyblue')
    ax.set_xlabel("Score")
    ax.set_ylabel("Movies")
    ax.set_title("Recommended Movies and Their Scores")
    plt.gca().invert_yaxis()
    st.pyplot(fig)

def show():
    """
    Displays a simple recommendation system interface for selecting movie genres.

    Users can select their favorite movie genres from a list, specify the number of recommendations,
    and generate movie recommendations with random scores. The recommendations are sorted by score
    and displayed in a table and a bar chart.
    """
    st.title("🎬 Simple Recommendation System")

    st.subheader("Select Your Favorite Movie Genres")
    genres = ["Action", "Comedy", "Drama", "Sci-Fi", "Horror"]
    selected_genres = st.multiselect("Choose genres:", genres)
    
    num_recommendations = st.slider("Number of recommendations:", 1, 20, 5)
    
    if selected_genres:
        recommendations = get_recommendations(selected_genres, num_recommendations)
        
        st.subheader("🎥 Recommended Movies")
        df = pd.DataFrame(recommendations.items(), columns=["Movie", "Score"])
        st.table(df)
        
        st.subheader("📊 Recommendation Scores")
        plot_scores(recommendations)
    else:
        st.info("Please select at least one genre to get recommendations.")
