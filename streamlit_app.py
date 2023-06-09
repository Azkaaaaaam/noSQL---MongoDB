import streamlit as st
import pymongo
import sqlite3

#client = pymongo.MongoClient("mongodb+srv://kamounazzap:Hello123.@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority", server_api=ServerApi('1'))
#db = client.test
#mongodb://_:<API-KEY>@global.aws.realm.mongodb.com:27020/?authMechanism=PLAIN&authSource=%24external&ssl=true&appName=data-mnfje:Cluster0:api-key


client = pymongo.MongoClient("mongodb+srv://streamlit:streamlit@cluster0.9gb1qb6.mongodb.net/?retryWrites=true&w=majority")

# Access the "moviesds" database.
db = client["moviesds"]

# Access the "moviesds" collection.
movies_collection = db["moviesds"]

def display_movie_info(selected_movie_info):
    st.header("Movie Info:")
    if selected_movie_info is not None:
        data = {
            "Title": [selected_movie_info['title']],
            "Year": [selected_movie_info['year']],
            "Genre": [selected_movie_info['genre']],
            "Nationality": [selected_movie_info['nationality']],
            "Average Rating": [selected_movie_info['average_rating']]
        }
        st.table(data)
    else:
        st.write("No movie selected.")


def add_comment(selected_movie_info):
    nickname = st.text_input("Enter your nickname", value="Anonymous")
    comment = st.text_input("Enter your comment")
    if st.button("Add Comment"):
        if nickname != "Anonymous" and not comment:
            st.error("You must write a comment.")
        elif comment:
            comments = selected_movie_info.get("comments", [])
            if not isinstance(comments, list):
                comments = [comments]
            comments.append({"nickname": nickname, "comment": comment})
            movies_collection.update_one({"_id": selected_movie_info["_id"]}, {"$set": {"comments": comments}})
            st.success("Comment added.")

def update_rating(selected_movie_info, rating):
    old_average_rating = selected_movie_info.get("average_rating", 0)
    ratings = selected_movie_info.get("ratings", [])
    ratings.append(rating)
    new_average_rating = round(sum(ratings) / len(ratings), 2)
    movies_collection.update_one(
        {"_id": selected_movie_info["_id"]},
        {"$set": {"average_rating": new_average_rating, "ratings": ratings}}
    )
    st.success("Rating added.")
    return old_average_rating, new_average_rating


def delete_movie():
    movie_titles = [movie["title"] for movie in movies_collection.find()]
    movie_to_delete = st.selectbox("Select a movie to delete", movie_titles)
    if st.button("Delete"):
        movies_collection.delete_one({"title": movie_to_delete})
        st.success(f"{movie_to_delete} has been deleted from the database.")


def add_new_movie():
    title = st.text_input("Title")
    year = st.number_input("year", min_value=1800, max_value=2100)
    genre = st.text_input("genre")
    nationality = st.text_input("Nationality")
    if st.button("Add movie"):
        new_movie = {"title": title, "year": year, "genre": genre, "nationality": nationality,
                     "average_rating": 0, "comments": [], "ratings": []}
        movies_collection.insert_one(new_movie)
        st.success(f"{title} has been added to the database.")


def display_comments(selected_movie_info):
    comments = selected_movie_info.get("comments", [])
    st.write("### Comments")
    data = [["Nickname", "Comment"]]
    for comment in comments:
        if isinstance(comment, dict):
            data.append([comment['nickname'], comment['comment']])
        else:
            st.write("No comments yet.")
    st.table(data)


def main():
    st.set_page_config(page_title="Movie Database", page_icon=":movie_camera:")

    # Sidebar options
    options = ["View All Movies", "Add Movie", "Delete Movie", "Rate Movie"]
    choice = st.sidebar.selectbox("Select an option", options)

    # View all movies
    if choice == "View All Movies":
        st.header("All Movies")
        movies = movies_collection.find()
        for movie in movies:
            selected_movie_info = movie
            display_movie_info(selected_movie_info)
            display_comments(selected_movie_info)
            st.write("\n")

    # Add movie
    elif choice == "Add Movie":
        st.header("Add Movie")
        add_new_movie()

    # Delete movie
    elif choice == "Delete Movie":
        st.header("Delete Movie")
        delete_movie()
    elif choice == "Rate Movie":
        movie_titles = [movie["title"] for movie in movies_collection.find()]
        selected_movie_title = st.selectbox("Select a movie", movie_titles)
        selected_movie_info = movies_collection.find_one({"title": selected_movie_title})
        display_movie_info(selected_movie_info)
        display_comments(selected_movie_info)

        st.write("\n")
        col1, col2 = st.columns(2)

    # Column 1: Add Comment
        with col1:
           # if choice == "Add Comment":
            st.header("Comment a Movie")
            add_comment(selected_movie_info)

        # Column 2: Rate Movie
        with col2:
            st.header("Rate Movie")
            rating = st.slider("Rate the movie", min_value=1, max_value=10, step=1)
            submit_rating = st.button("Submit Rating")
            if submit_rating:
                old_rating, new_rating = update_rating(selected_movie_info, rating)
                st.write(f"Old average rating: {old_rating}")
                st.write(f"New average rating: {new_rating}")

    # View movie details
    st.sidebar.write("\n")
    movie_titles = [movie["title"] for movie in movies_collection.find()]
    selected_movie_title = st.sidebar.selectbox("Select a movie", movie_titles, key="unique_key")
    selected_movie_info = movies_collection.find_one({"title": selected_movie_title})
    st.sidebar.write("\n")


main()
    
