
import pandas as pd
from pathlib import Path

# Input files
DATA_FOLDER = Path("movielens")
movies_path = DATA_FOLDER / "movies.csv"
ratings_path = DATA_FOLDER / "ratings.csv"

# Check that both files exist
if not movies_path.exists() or not ratings_path.exists():
    raise FileNotFoundError(
        "Please put movies.csv and ratings.csv inside the movielens folder."
    )

# Load the MovieLens dataset
movies = pd.read_csv(movies_path)
ratings = pd.read_csv(ratings_path)

print("Movies loaded:", len(movies))
print("Ratings loaded:", len(ratings))

# Calculate average rating and number of votes per movie
rating_summary = ratings.groupby("movieId").agg(
    average_rating=("rating", "mean"),
    votes=("rating", "count")
).reset_index()

# Combine movie information and rating statistics
data = movies.merge(rating_summary, on="movieId", how="left")

# Extract release year from the end of the movie title
data["year"] = pd.to_numeric(
    data["title"].str.extract(r"\((\d{4})\)\s*$")[0],
    errors="coerce"
)

# Convert MovieLens ratings from a 5-point scale to a 10-point scale
data["rating"] = (data["average_rating"] * 2).round(2)
data["votes"] = data["votes"].fillna(0).astype(int)

# Keep one row per movie and preserve all its genres
data["genre"] = data["genres"].fillna("(no genres listed)")
data["title"] = data["title"].str.replace(
    r"\s*\(\d{4}\)\s*$", "", regex=True
)

# Save a clean movie-level dataset
output = data[["title", "genre", "year", "rating", "votes"]].copy()
output.to_csv("movies_real.csv", index=False)

# Also prepare one row per movie-genre for genre analysis
genre_data = data[["movieId", "title", "genres", "year", "rating", "votes"]].copy()
genre_data["genre"] = genre_data["genres"].fillna("").str.split("|")
genre_data = genre_data.explode("genre")
genre_data = genre_data[
    (genre_data["genre"] != "") &
    (genre_data["genre"] != "(no genres listed)")
]
genre_data = genre_data[
    ["movieId", "title", "genre", "year", "rating", "votes"]
]
genre_data.to_csv("genre_data.csv", index=False)

print("\nData preparation completed!")
print("Created movies_real.csv:", len(output), "movies")
print("Created genre_data.csv:", len(genre_data), "movie-genre entries")
print("\nPreview:")
print(output.head())
