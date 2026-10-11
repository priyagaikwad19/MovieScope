
import pandas as pd
from pathlib import Path

# File locations
input_file = Path("indian_data/bollywood_full.csv")
output_file = Path("indian_data/indian_movies.csv")

print("Loading Bollywood movie dataset...")

# Read original dataset
df = pd.read_csv(input_file)

# Choose the best available movie title
title = df["title_x"].fillna(df["title_y"])
title = title.fillna(df["original_title"])

# Prepare a clean dataset for MovieScope
clean_df = pd.DataFrame({
    "title": title,
    "genre": df["genres"],
    "year": pd.to_numeric(
        df["year_of_release"], errors="coerce"
    ),
    "rating": pd.to_numeric(
        df["imdb_rating"], errors="coerce"
    ),
    "votes": pd.to_numeric(
        df["imdb_votes"], errors="coerce"
    ).fillna(0),
    "source": "Bollywood (IMDb)",
    "poster": df["poster_path"],
    "actors": df["actors"],
    "imdb_id": df["imdb_id"]
})

# Clean up missing values and duplicate records
clean_df["title"] = clean_df["title"].astype("string").str.strip()
clean_df["genre"] = clean_df["genre"].fillna("Unknown")

clean_df = clean_df.dropna(subset=["title", "rating"])
clean_df = clean_df[clean_df["title"] != ""]
clean_df = clean_df.drop_duplicates(subset=["imdb_id"], keep="first")

# Keep valid IMDb ratings
clean_df = clean_df[
    clean_df["rating"].between(0, 10)
].copy()

# Save cleaned data
output_file.parent.mkdir(parents=True, exist_ok=True)
clean_df.to_csv(output_file, index=False)

print("\nBollywood dataset prepared successfully!")
print(f"Movies saved: {len(clean_df):,}")
print(f"Output file: {output_file}")
print("\nFirst five movies:")
print(clean_df[["title", "genre", "year", "rating", "votes"]].head())
