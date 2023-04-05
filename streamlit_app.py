import streamlit as st
def add_new_movie(movies):
    title = st.sidebar.text_input("Title")
    released_year = st.sidebar.number_input("Released year", min_value=1800, max_value=2100)
    kind = st.sidebar.text_input("Kind")
    nationality = st.sidebar.text_input("Nationality")
    if st.sidebar.button("Add movie"):
        new_movie = {"title": title, "released_year": released_year, "kind": kind, "nationality": nationality, "average_ranking": 0, "comments": [], "num_reviews": 0}
        movies.append(new_movie)
        st.sidebar.success(f"{title} has been added to the database.")
    return movies


def display_movie_info(movie):
    st.write(f"Title: {movie['title']}")
    st.write(f"Released Year: {movie['released_year']}")
    st.write(f"Kind: {movie['kind']}")
    st.write(f"Nationality: {movie['nationality']}")
    st.write(f"Average Ranking: {movie['average_ranking']}")


def add_comment(selected_movie_info):
    nickname = st.text_input("Enter your nickname", value="Anonymous")
    comment = st.text_input("Enter your comment")
    if st.button("Add Comment"):
        if nickname != "Anonymous" and not comment:
            st.error("You must write a comment.")
        elif comment:
            selected_movie_info["comments"].append({"nickname": nickname, "comment": comment})


def display_comments(selected_movie_info):
    st.write("Comments:")
    for comment in selected_movie_info["comments"]:
        if isinstance(comment, str):
            st.write(f"Anonymous: {comment}")
        elif isinstance(comment, dict) and "nickname" in comment and "comment" in comment:
            st.write(f"{comment['nickname']}: {comment['comment']}")


def rate_movie(selected_movie_info):
    if st.button("Submit Review"):
        rating = st.number_input("Enter your rating (0-5)", min_value=0, max_value=5)
        num_reviews = selected_movie_info["num_reviews"]
        current_ranking = selected_movie_info["average_ranking"]
        new_ranking = (current_ranking * num_reviews + rating) / (num_reviews + 1)
        selected_movie_info["average_ranking"] = new_ranking
        selected_movie_info["num_reviews"] = num_reviews + 1
        st.success(f"You rated {selected_movie_info['title']} {rating} stars.")


def delete_movie(movies, selected_movie_info):
    movies.remove(selected_movie_info)
    st.success(f"{selected_movie_info['title']} has been deleted from the database.")
    return movies

def main():
    st.title("Movie Database")
    st.header("Select a movie from the dropdown list to view its details, rate it, or delete it.")
    
    # List of example movies
    movies = [
        {"title": "The Shawshank Redemption", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.7, "comments": ["Great movie!", "One of my all-time favorites."]},
        {"title": "The Godfather", "released_year": 1972, "kind": "Crime", "nationality": "USA", "average_ranking": 4.8, "comments": ["A classic!", "Marlon Brando was amazing."]},
        {"title": "The Dark Knight", "released_year": 2008, "kind": "Action", "nationality": "USA", "average_ranking": 4.6, "comments": ["Heath Ledger's performance was outstanding.", "Great soundtrack."]},
        {"title": "The Lord of the Rings: The Fellowship of the Ring", "released_year": 2001, "kind": "Adventure", "nationality": "USA", "average_ranking": 4.5, "comments": ["Epic story!", "The special effects were amazing."]},
        {"title": "Forrest Gump", "released_year": 1994, "kind": "Drama", "nationality": "USA", "average_ranking": 4.4, "comments": ["Tom Hanks was perfect for this role.", "Heartwarming story."]}
        ]
    # Create a list of movie titles for the dropdown menu
    movie_titles = [movie["title"] for movie in movies]

    # Create a dropdown menu to select a movie
    selected_movie_title = st.selectbox("Select a movie", movie_titles)

    # Find the selected movie in the list of movies
    selected_movie_info = None
    if selected_movie_title:
        selected_movie_info = next((movie for movie in movies if movie["title"] == selected_movie_title), None)
        if selected_movie_info:
            display_movie_info(selected_movie_info)
        else:
            st.error("Error: Could not find movie in database.")
main()

    
