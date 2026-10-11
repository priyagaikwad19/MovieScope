
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="MovieScope",
    page_icon="🎬",
    layout="wide"
)


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top left, #29204D 0%, transparent 42%),
        linear-gradient(135deg, #0B1020, #15172B 65%, #201638);
    color: #F8FAFF;
    font-family: 'Inter', sans-serif;
}

/* Remove the built-in top bar that was overlapping the page content */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
}
[data-testid="stDecoration"] {
    display: none !important;
} 
[data-testid="stToolbar"] {
    display: none !important;
}

.block-container {
    max-width: 1150px;
    padding-top: 7rem !important;
}

/* Main headings and regular text */
h1, h2, h3, h4, p, li, label,
[data-testid="stMarkdownContainer"] {
    color: #F3F4FF;
}

.movie-logo {
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1.5px;
    color: #FFD779 !important;
}

.movie-tagline {
    color: #D0D4E8 !important;
    font-size: 15px;
    line-height: 1.8;
}

/* Input labels */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
.stTextInput label,
.stSelectbox label,
.stSlider label,
.stRadio label {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Username and password input fields */
.stTextInput input,
.stNumberInput input,
.stDateInput input {
    background-color: #F5F6FC !important;
    color: #17192B !important;
    border: 1px solid #A8ADCC !important;
    border-radius: 9px !important;
    caret-color: #17192B !important;
}

.stTextInput input::placeholder,
.stNumberInput input::placeholder {
    color: #62677D !important;
    opacity: 1 !important;
}

/* Dropdowns and select controls */
.stSelectbox [data-baseweb="select"] > div {
    background-color: #F5F6FC !important;
    color: #17192B !important;
    border-color: #A8ADCC !important;
}

.stSelectbox [data-baseweb="select"] * {
    color: #17192B !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #15182A;
}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #F3F4FF;
}

/* Metric cards and rating numbers */
[data-testid="stMetric"] {
    background: #222740;
    border: 1px solid #515A7D;
    border-radius: 16px;
    padding: 18px;
}

[data-testid="stMetricLabel"] p {
    color: #D9DDF0 !important;
    font-size: 14px !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #FFD779 !important;
    font-size: 32px !important;
    font-weight: 800 !important;
}

[data-testid="stMetricDelta"] {
    color: #A9F0C4 !important;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(90deg, #8B5CF6, #B58AFB);
    color: #FFFFFF !important;
    border: 1px solid #C4A7FF;
    border-radius: 10px;
    font-weight: 700;
    min-height: 45px;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    border: 1px solid #FFD779;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Tables */
[data-testid="stDataFrame"] {
    border: 1px solid #454C6B;
    border-radius: 10px;
}

/* Captions and helper text */
.stCaption, [data-testid="stCaptionContainer"] {
    color: #C4C9DF !important;
}

/* Slider text and ticks */
.stSlider [data-testid="stTickBar"] {
    color: #F3F4FF !important;
}

/* Tabs */
.stTabs [data-baseweb="tab"] {
    color: #E6E8F5 !important;
}

.stTabs [aria-selected="true"] {
    color: #FFD779 !important;
}

/* -------- MOVIESCOPE VISUAL POLISH -------- */
/* Keep the login page clear of Streamlit's built-in top bar. */
header[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"] {
    display: none !important;
}
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
section.main {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
[data-testid="stMainBlockContainer"] {
    padding-top: 7rem !important;
}
[data-testid="stDataFrame"] {
    background: #171D31 !important;
    border: 1px solid #424B6B !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 24px rgba(0,0,0,.18) !important;
}
[data-testid="stDataFrame"] iframe {
    background: #171D31 !important;
}
[data-testid="stTable"] {
    background: #171D31 !important;
    color: #F4F5FA !important;
}
[data-testid="stTable"] table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
}
[data-testid="stTable"] thead tr th {
    background: #343052 !important;
    color: #FFE09A !important;
    border-bottom: 1px solid #5A527A !important;
}
[data-testid="stTable"] tbody tr:nth-child(odd) {
    background: #202740 !important;
}
[data-testid="stTable"] tbody tr:nth-child(even) {
    background: #171D31 !important;
}
[data-testid="stTable"] tbody tr td {
    color: #F4F5FA !important;
    border-bottom: 1px solid #343B55 !important;
}
[data-testid="stDataFrame"] [role="grid"] {
    border-radius: 12px !important;
}
/* Make charts and their surrounding containers feel intentional. */
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has([data-testid="stImage"]),
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has([data-testid="stVegaLiteChart"]),
[data-testid="stVerticalBlock"] > [data-testid="stElementContainer"]:has([data-testid="stArrowVegaLiteChart"]) {
    border-radius: 14px;
}
div[data-testid="stPlotlyChart"],
div[data-testid="stVegaLiteChart"],
div[data-testid="stArrowVegaLiteChart"] {
    background: #171D31 !important;
    border: 1px solid #343B55 !important;
    border-radius: 14px !important;
    padding: 8px !important;
}
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}
button[kind="header"] {
    color: #F4F5FA !important;
}
/* Keep the menu and toolbar controls legible; do not hide Streamlit controls. */
[data-testid="stToolbar"] button,
header[data-testid="stHeader"] button {
    color: #F4F5FA !important;
}

</style>
""", unsafe_allow_html=True)

# -------- MOVIESCOPE LOGIN --------
# Demo-only authentication: accounts are stored in session memory, not securely persisted.

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "demo_users" not in st.session_state:
    st.session_state.demo_users = {
        "student": "movie123"
    }

if "auth_page" not in st.session_state:
    st.session_state.auth_page = "Login"

if not st.session_state.authenticated:
    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown(
            '<div class="movie-logo">🎬 MovieScope</div>',
            unsafe_allow_html=True
        )
        st.markdown(
            "### Discover the stories behind the ratings.",
        )
        st.markdown(
            '<p class="movie-tagline">'
            'Explore movie ratings, uncover genre trends, compare films, '
            'and discover hidden gems with data science.'
            '</p>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<span class="feature-chip">📊 Smart Analytics</span>'
            '<span class="feature-chip">🎭 Genre Explorer</span>'
            '<span class="feature-chip">💎 Hidden Gems</span>'
            '<span class="feature-chip">⚔️ Movie Face-Off</span>',
            unsafe_allow_html=True
        )

        st.markdown("")
        st.markdown("#### Your next favourite movie is waiting.")
        st.caption("Powered by Python • Pandas • Streamlit • MovieLens data")

    with right:
        st.markdown("## Welcome to MovieScope")
        st.caption("Sign in or create a demo account to explore.")

        page = st.radio(
            "Choose a page",
            ["Login", "Register"],
            horizontal=True,
            key="login_register_choice",
            label_visibility="collapsed"
        )

        username = st.text_input("Username", key="auth_username")
        password = st.text_input(
            "Password",
            type="password",
            key="auth_password"
        )

        if page == "Login":
            if st.button("Sign In →", width="stretch"):
                users = st.session_state.demo_users

                if users.get(username) == password and username:
                    st.session_state.authenticated = True
                    st.session_state.current_user = username
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")

            st.info("Demo login: username `student`, password `movie123`")

        else:
            confirm = st.text_input(
                "Confirm password",
                type="password",
                key="confirm_password"
            )

            if st.button("Create Account →", width="stretch"):
                users = st.session_state.demo_users

                if not username.strip() or not password:
                    st.warning("Enter a username and password.")
                elif username in users:
                    st.warning("That username already exists.")
                elif len(password) < 6:
                    st.warning("Use at least 6 characters for this demo.")
                elif password != confirm:
                    st.error("The passwords do not match.")
                else:
                    users[username] = password
                    st.success("Account created! Switch to Login to sign in.")


    st.stop()

# -------- MAIN DASHBOARD STARTS BELOW --------


# -------- MOVIESCOPE DASHBOARD HEADER --------
st.markdown("""
<div style="
    padding: 26px 28px;
    border-radius: 18px;
    background: linear-gradient(110deg, #1e293b, #25344d);
    border: 1px solid #475569;
    margin-bottom: 24px;
">
    <div style="color:#fbbf24; font-size:13px; font-weight:700;
                letter-spacing:2px;">
        FUNDAMENTALS OF DATA SCIENCE
    </div>
    <h1 style="margin:10px 0 8px; color:#ffffff;">
        🎬 MovieScope
    </h1>
    <p style="color:#cbd5e1; font-size:16px; margin-bottom:0;">
        Explore movie ratings, discover hidden gems, compare genres,
        and uncover insights from MovieLens and Bollywood cinema data.
    </p>
</div>
""", unsafe_allow_html=True)




# ---------------- CHART THEME ----------------
sns.set_theme(style="darkgrid", context="notebook", palette="husl")
sns.set_palette(["#A78BFA", "#38BDF8", "#FBBF24", "#34D399", "#FB7185", "#F97316"])

plt.rcParams["figure.facecolor"] = "#1C2135"
plt.rcParams["axes.facecolor"] = "#1C2135"
plt.rcParams["axes.edgecolor"] = "#596078"
plt.rcParams["axes.labelcolor"] = "#F4F5FA"
plt.rcParams["xtick.color"] = "#F4F5FA"
plt.rcParams["ytick.color"] = "#F4F5FA"
plt.rcParams["text.color"] = "#F4F5FA"
plt.rcParams["grid.color"] = "#394057"


# ---------------- LOAD REAL DATA ----------------
@st.cache_data
def load_data():
    movies = pd.read_csv("movies_real.csv")
    genres = pd.read_csv("genre_data.csv")

    movies["title"] = movies["title"].fillna("Unknown")
    movies["genre"] = movies["genre"].fillna("(no genres listed)")
    movies["rating"] = pd.to_numeric(
        movies["rating"], errors="coerce"
    )
    movies["votes"] = pd.to_numeric(
        movies["votes"], errors="coerce"
    ).fillna(0)

    genres["title"] = genres["title"].fillna("Unknown")
    genres["genre"] = genres["genre"].fillna("Unknown")
    genres["rating"] = pd.to_numeric(
        genres["rating"], errors="coerce"
    )
    genres["votes"] = pd.to_numeric(
        genres["votes"], errors="coerce"
    ).fillna(0)

    movies = movies.dropna(subset=["rating"]).copy()
    genres = genres.dropna(subset=["rating"]).copy()

    # Exclude movies without a meaningful genre from genre charts
    genres = genres[
        ~genres["genre"].isin(["(no genres listed)", "Unknown", ""])
    ].copy()

    return movies, genres


if not Path("movies_real.csv").exists() or not Path("genre_data.csv").exists():
    st.error(
        "Data files are missing. Run 'python prepare_data.py' first."
    )
    st.stop()

df, genre_data = load_data()


# -------- LOAD INDIAN MOVIE DATA --------

@st.cache_data
def load_indian_movies():
    return pd.read_csv("indian_data/indian_movies.csv")

indian_df = load_indian_movies()

# Keep ratings and vote counts numeric
indian_df["rating"] = pd.to_numeric(
    indian_df["rating"], errors="coerce"
)
indian_df["votes"] = pd.to_numeric(
    indian_df["votes"], errors="coerce"
).fillna(0)

indian_df["year"] = pd.to_numeric(
    indian_df["year"], errors="coerce"
)

indian_df = indian_df.dropna(subset=["title", "rating"])

st.caption(
    f"🇮🇳 Indian cinema database loaded: "
    f"{len(indian_df):,} movies"
)



# ---------------- HEADER ----------------
st.title("🎬 MovieScope")
st.subheader("Movie Rating & Genre Popularity Analyzer")
st.write(
    "Explore movie ratings, compare genres, and discover "
    "interesting patterns in real movie-rating data."
)
st.caption("Dataset: MovieLens Small | Ratings converted to a 10-point scale")

st.divider()


# ---------------- SIDEBAR ----------------
st.sidebar.title("🎞️ Explore Movies")

if st.sidebar.button("🔄 Rerun / Refresh dashboard", width="stretch"):
    st.rerun()


available_genres = sorted(genre_data["genre"].unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Choose a genre",
    ["All Genres"] + available_genres
)

min_rating = st.sidebar.slider(
    "Minimum movie rating",
    min_value=0.0,
    max_value=10.0,
    value=0.0,
    step=0.5
)

# First filter by rating. Each movie stays unique in df.
rating_filtered = df[df["rating"] >= min_rating].copy()

# Use genre_data to identify movies belonging to the selected genre.
if selected_genre == "All Genres":
    filtered = rating_filtered.copy()
else:
    matching_titles = genre_data.loc[
        (genre_data["genre"] == selected_genre)
        & (genre_data["rating"] >= min_rating),
        "title"
    ].unique()

    filtered = rating_filtered[
        rating_filtered["title"].isin(matching_titles)
    ].copy()

# Find genre records for movies that meet the rating threshold.
# These records allow one movie to contribute to each of its genres.
eligible_genres = genre_data[
    genre_data["rating"] >= min_rating
].copy()

if selected_genre != "All Genres":
    eligible_genres = eligible_genres[
        eligible_genres["genre"] == selected_genre
    ]
    st.sidebar.markdown("---")
st.sidebar.caption(
    f"Signed in as: {st.session_state.get('current_user', 'User')}"
)

if st.sidebar.button("Log out", width="stretch"):
    st.session_state.authenticated = False
    st.session_state.pop("current_user", None)
    st.rerun()


# ---------------- SUMMARY CARDS ----------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("🎥 Total Movies", f"{len(filtered):,}")

if not filtered.empty:
    c2.metric(
        "⭐ Average Rating",
        f"{filtered['rating'].mean():.2f}/10"
    )
    c3.metric(
        "🏆 Highest Rating",
        f"{filtered['rating'].max():.1f}/10"
    )
    c4.metric(
        "🗳️ Total Votes",
        f"{int(filtered['votes'].sum()):,}"
    )
else:
    c2.metric("⭐ Average Rating", "N/A")
    c3.metric("🏆 Highest Rating", "N/A")
    c4.metric("🗳️ Total Votes", "0")

st.divider()


if filtered.empty:
    st.warning(
        "No movies match your filters. Try selecting a lower minimum rating."
    )

else:
     
    # ---------------- PROFESSIONAL CHARTS ----------------
    left, right = st.columns(2, gap="large")

    # BAR CHART: Average rating by genre
    with left:
        st.subheader("Average Rating by Genre")
        st.caption("Compare audience ratings across movie genres")

        genre_ratings = (
            eligible_genres.groupby("genre")["rating"]
            .mean()
            .sort_values()
        )

        if not genre_ratings.empty:
            fig, ax = plt.subplots(figsize=(8, 5))

            colors = [
                "#E5C07B" if genre == selected_genre else "#5479A8"
                for genre in genre_ratings.index
            ]

            bars = ax.barh(
                genre_ratings.index,
                genre_ratings.values,
                color=colors,
                height=0.62
            )

            ax.set_xlim(0, 10)
            ax.set_xlabel("Average rating / 10", labelpad=10)
            ax.set_ylabel("")
            ax.set_title("Audience Rating", loc="left", pad=14)
            ax.grid(axis="x", alpha=0.22)
            ax.grid(axis="y", visible=False)
            ax.set_axisbelow(True)

            for bar, value in zip(bars, genre_ratings.values):
                ax.text(
                    value + 0.12,
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:.2f}",
                    va="center",
                    fontsize=9,
                    color="#F4F5FA"
                )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_alpha(0.3)
            ax.tick_params(axis="y", length=0, labelsize=9)
            ax.tick_params(axis="x", labelsize=9)

            fig.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        else:
            st.info("No genre rating data is available.")

    # BAR CHART: Number of movies by genre
    with right:
        st.subheader("Genre Popularity")
        st.caption("Number of unique movies associated with each genre")

        genre_counts = (
            eligible_genres.groupby("genre")["movieId"]
            .nunique()
            .sort_values()
        )

        if not genre_counts.empty:
            fig, ax = plt.subplots(figsize=(8, 5))

            colors = [
                "#E5C07B" if genre == selected_genre else "#5479A8"
                for genre in genre_counts.index
            ]

            bars = ax.barh(
                genre_counts.index,
                genre_counts.values,
                color=colors,
                height=0.62
            )

            ax.set_xlabel("Number of movies", labelpad=10)
            ax.set_ylabel("")
            ax.set_title("Movies per Genre", loc="left", pad=14)
            ax.grid(axis="x", alpha=0.22)
            ax.grid(axis="y", visible=False)
            ax.set_axisbelow(True)

            for bar, value in zip(bars, genre_counts.values):
                ax.text(
                    value + max(genre_counts.max() * 0.01, 1),
                    bar.get_y() + bar.get_height() / 2,
                    f"{value:,}",
                    va="center",
                    fontsize=9,
                    color="#F4F5FA"
                )

            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.spines["bottom"].set_alpha(0.3)
            ax.tick_params(axis="y", length=0, labelsize=9)
            ax.tick_params(axis="x", labelsize=9)

            fig.tight_layout()
            st.pyplot(fig, width="stretch")
            plt.close(fig)
        else:
            st.info("No genre count data is available.")

    # ---------------- TOP MOVIES ----------------
    
# -------- TOP-RATED MOVIES --------

st.subheader("🏆 Top-Rated Movies")

minimum_votes = st.select_slider(
    "Minimum number of votes",
    options=[1, 5, 10, 25, 50, 100, 250, 500],
    value=100
)

top_movies = filtered[
    filtered["votes"] >= minimum_votes
].sort_values(
    ["rating", "votes"],
    ascending=[False, False]
).head(10)

if top_movies.empty:
    st.info("No movies match this vote threshold and your current filters.")
else:
    display_movies = top_movies[
        ["title", "genre", "year", "rating", "votes"]
    ].copy()

    display_movies["rating"] = display_movies["rating"].map(
        lambda value: f"⭐ {value:.1f}/10"
    )

    st.dataframe(
        display_movies,
        width="stretch",
        hide_index=True
    ,
)
    
# -------- MOVIE FACE-OFF --------

st.markdown("---")
st.header("⚔️ Movie Face-Off")
st.write("Choose two movies and compare their ratings and popularity.")

# Use movies that meet the current minimum-rating filter
comparison_data = df.copy()

if "votes" not in comparison_data.columns:
    st.error("The movie dataset must contain a votes column.")
else:
    comparison_data = comparison_data.dropna(
        subset=["title", "rating"]
    )

    # Keep one option for every unique movie title
    movie_options = sorted(
        comparison_data["title"].astype(str).unique().tolist()
    )

    if len(movie_options) >= 2:
        col1, col2 = st.columns(2)

        with col1:
            movie_a = st.selectbox(
                "🎬 Select Movie A",
                movie_options,
                index=0,
                key="faceoff_movie_a"
            )

        with col2:
            default_b = 1 if len(movie_options) > 1 else 0
            movie_b = st.selectbox(
                "🎬 Select Movie B",
                movie_options,
                index=default_b,
                key="faceoff_movie_b"
            )

        if movie_a == movie_b:
            st.warning("Please select two different movies.")
        else:
            a = comparison_data[
                comparison_data["title"].astype(str) == movie_a
            ].iloc[0]

            b = comparison_data[
                comparison_data["title"].astype(str) == movie_b
            ].iloc[0]

            left, right = st.columns(2, gap="large")

            with left:
                st.subheader(f"🎞️ {movie_a}")
                st.metric("⭐ Rating", f"{a['rating']:.1f}/10")
                st.metric("👥 Votes", f"{int(a['votes']):,}")
                st.write(f"**Year:** {a['year']}")
                st.write(f"**Genre:** {a['genre']}")

            with right:
                st.subheader(f"🎞️ {movie_b}")
                st.metric("⭐ Rating", f"{b['rating']:.1f}/10")
                st.metric("👥 Votes", f"{int(b['votes']):,}")
                st.write(f"**Year:** {b['year']}")
                st.write(f"**Genre:** {b['genre']}")

            st.markdown("### 🏆 Face-Off Result")

            if a["rating"] > b["rating"]:
                st.success(
                    f"🏆 {movie_a} has the higher average rating!"
                )
            elif b["rating"] > a["rating"]:
                st.success(
                    f"🏆 {movie_b} has the higher average rating!"
                )
            else:
                st.info("It's a tie! Both movies have the same average rating.")

            st.caption(
                "Note: Ratings show audience averages. Vote counts provide "
                "context; a higher rating does not automatically mean a "
                "movie is better for every viewer."
            )
    else:
        st.warning("At least two movies are required for comparison.")

        
# -------- HIDDEN GEMS FINDER --------

st.markdown("---")
st.header("💎 Hidden Gems Finder")
st.write(
    "Discover highly rated movies that have received fewer audience votes."
)

gem_col1, gem_col2, gem_col3 = st.columns(3)

with gem_col1:
    gem_min_rating = st.slider(
        "Minimum rating",
        min_value=5.0,
        max_value=10.0,
        value=7.5,
        step=0.5,
        key="gem_rating"
    )

with gem_col2:
    gem_min_votes = st.select_slider(
        "Minimum votes",
        options=[1, 10, 25, 50, 100, 200],
        value=10,
        key="gem_min_votes"
    )

with gem_col3:
    gem_max_votes = st.select_slider(
        "Maximum votes",
        options=[50, 100, 200, 300, 500, 750, 1000],
        value=300,
        key="gem_max_votes"
    )

gem_sort = st.selectbox(
    "Sort hidden gems by",
    [
        "Highest rating",
        "Fewest votes",
        "Most votes",
        "Oldest movies",
        "Newest movies"
    ],
    key="gem_sort"
)

# Apply every filter to the actual movie table
gems = df[
    (df["rating"] >= gem_min_rating) &
    (df["votes"] >= gem_min_votes) &
    (df["votes"] <= gem_max_votes)
].copy()

gems = gems.drop_duplicates(subset=["title"])

# Sort the actual results table
if gem_sort == "Highest rating":
    gems = gems.sort_values(
        ["rating", "votes"], ascending=[False, False]
    )
elif gem_sort == "Fewest votes":
    gems = gems.sort_values(
        ["votes", "rating"], ascending=[True, False]
    )
elif gem_sort == "Most votes":
    gems = gems.sort_values(
        ["votes", "rating"], ascending=[False, False]
    )
elif gem_sort == "Oldest movies":
    gems = gems.sort_values("year", ascending=True)
else:
    gems = gems.sort_values("year", ascending=False)

st.markdown("### 🎬 Your Hidden Gems")

if gems.empty:
    st.warning(
        "No movies match these filters. Lower the minimum rating "
        "or adjust the vote range."
    )
else:
    st.success(f"Found {len(gems):,} matching movies.")

    # Show more than 10 results, with a user-controlled limit
    display_limit = st.select_slider(
        "Number of movies to display",
        options=[10, 20, 30, 50],
        value=20,
        key="gem_display_limit"
    )

    visible_gems = gems.head(display_limit)

    st.dataframe(
        visible_gems[
            ["title", "genre", "year", "rating", "votes"]
        ],
        width="stretch",
        hide_index=True
    ,
)

    st.caption(
        f"Showing {len(visible_gems)} of {len(gems):,} matching movies. "
        "Movies with fewer votes have less reliable average ratings."
    )

# -------- MOVIE MATCHMAKER --------

st.markdown("---")
st.header("🎯 Movie Matchmaker")
st.write(
    "Find movies that match your taste! Choose your preferred genre, "
    "rating, release years, and number of recommendations."
)

# Prepare movie data
match_data = df.copy()
match_data = match_data.dropna(subset=["title", "rating"])
match_data["year"] = pd.to_numeric(match_data["year"], errors="coerce")
match_data["rating"] = pd.to_numeric(match_data["rating"], errors="coerce")
match_data["votes"] = pd.to_numeric(match_data["votes"], errors="coerce").fillna(0)
match_data = match_data.dropna(subset=["rating"])

# Get available genres
available_genres = sorted(
    genre_data["genre"].dropna().astype(str).unique().tolist()
)
available_genres = [
    genre for genre in available_genres
    if genre.lower() not in ["nan", "(no genres listed)", "unknown"]
]

# User preferences
match_col1, match_col2 = st.columns(2)

with match_col1:
    preferred_genre = st.selectbox(
        "🎭 Choose your favourite genre",
        ["Any Genre"] + available_genres,
        key="match_genre"
    )

    preferred_rating = st.slider(
        "⭐ Minimum movie rating",
        min_value=0.0,
        max_value=10.0,
        value=7.0,
        step=0.5,
        key="match_rating"
    )

with match_col2:
    valid_years = match_data["year"].dropna()

    if not valid_years.empty:
        min_year = int(valid_years.min())
        max_year = int(valid_years.max())
    else:
        min_year, max_year = 1900, 2026

    year_range = st.slider(
        "📅 Release year range",
        min_value=min_year,
        max_value=max_year,
        value=(max(min_year, max_year - 30), max_year),
        key="match_years"
    )

    recommendation_count = st.selectbox(
        "🎬 Number of recommendations",
        [5, 10, 15, 20],
        index=1,
        key="match_count"
    )

# Apply preferences
recommendations = match_data[
    (match_data["rating"] >= preferred_rating)
].copy()

recommendations = recommendations[
    recommendations["year"].between(
        year_range[0], year_range[1]
    )
]

if preferred_genre != "Any Genre":
    matching_titles = genre_data.loc[
        genre_data["genre"] == preferred_genre, "title"
    ].astype(str).unique()

    recommendations = recommendations[
        recommendations["title"].astype(str).isin(matching_titles)
    ]

# Rank highly rated movies, using vote count as a secondary factor
recommendations = recommendations.sort_values(
    ["rating", "votes"], ascending=[False, False]
)

st.markdown("### 🍿 Your Recommended Movies")

if recommendations.empty:
    st.warning(
        "No movies match all your preferences. Try lowering the minimum "
        "rating or choosing a wider release-year range."
    )
else:
    st.success(
        f"Found {len(recommendations):,} movies matching your preferences!"
    )

    shown_recommendations = recommendations.head(recommendation_count)

    display_recommendations = shown_recommendations[
        ["title", "genre", "year", "rating", "votes"]
    ].copy()

    display_recommendations["year"] = (
        display_recommendations["year"].astype("Int64")
    )
    display_recommendations["rating"] = (
        display_recommendations["rating"].map(
            lambda value: f"⭐ {value:.1f}/10"
        )
    )

    st.dataframe(
        display_recommendations,
        width="stretch",
        hide_index=True
    ,
)

    st.caption(
        "Recommendations are ranked by average audience rating, with vote "
        "count used as a secondary factor. They are data-based suggestions, "
        "not a guarantee that you will personally enjoy every movie."
    )
    
# -------- INDIAN CINEMA EXPLORER --------

st.markdown("---")
st.header("🇮🇳 Indian Cinema Explorer")
st.write(
    "Explore Bollywood movies using IMDb ratings, genres, "
    "release years, and audience vote counts."
)

indian_explorer = indian_df.copy()

# Prepare genre options
indian_explorer["genre"] = (
    indian_explorer["genre"].fillna("Unknown").astype(str)
)

indian_genres = sorted({
    genre.strip()
    for genres in indian_explorer["genre"]
    for genre in genres.split("|")
    if genre.strip() and genre.strip().lower() != "unknown"
})

# Filters
india_col1, india_col2 = st.columns(2)

with india_col1:
    selected_indian_genre = st.selectbox(
        "🎭 Bollywood genre",
        ["All Genres"] + indian_genres,
        key="india_genre_filter"
    )

with india_col2:
    indian_sort = st.selectbox(
        "📊 Sort movies by",
        [
            "Highest IMDb rating",
            "Most votes",
            "Newest first",
            "Oldest first"
        ],
        key="india_sort"
    )

# Apply genre filter
if selected_indian_genre != "All Genres":
    indian_explorer = indian_explorer[
        indian_explorer["genre"].apply(
            lambda value: selected_indian_genre in value.split("|")
        )
    ].copy()

# Apply sorting
if indian_sort == "Highest IMDb rating":
    indian_explorer = indian_explorer.sort_values(
        ["rating", "votes"], ascending=[False, False]
    )
elif indian_sort == "Most votes":
    indian_explorer = indian_explorer.sort_values(
        "votes", ascending=False
    )
elif indian_sort == "Newest first":
    indian_explorer = indian_explorer.sort_values(
        "year", ascending=False, na_position="last"
    )
else:
    indian_explorer = indian_explorer.sort_values(
        "year", ascending=True, na_position="last"
    )

st.metric("🎬 Matching Bollywood movies", f"{len(indian_explorer):,}")

if indian_explorer.empty:
    st.info("No movies match this genre. Try another filter.")
else:
    display_count = st.selectbox(
        "Number of movies to display",
        [10, 20, 50, 100],
        index=1,
        key="india_display_count"
    )

    indian_display = indian_explorer.head(display_count)

    st.dataframe(
        indian_display[
            ["title", "genre", "year", "rating", "votes"]
        ].rename(columns={
            "title": "Movie",
            "genre": "Genres",
            "year": "Release Year",
            "rating": "IMDb Rating / 10",
            "votes": "IMDb Votes"
        }),
        width="stretch",
        hide_index=True
    ,
)

    # Optional poster preview
    poster_movies = indian_display[
        indian_display["poster"].notna()
        & (indian_display["poster"].astype(str).str.startswith("https://"))
    ]

    if not poster_movies.empty:
        st.markdown("### 🍿 Movie Poster Preview")
        poster_choice = st.selectbox(
            "Choose a movie to preview",
            poster_movies["title"].tolist(),
            key="india_poster_choice"
        )

        poster_row = poster_movies[
            poster_movies["title"] == poster_choice
        ].iloc[0]

        st.image(
            poster_row["poster"],
            caption=f"{poster_row['title']} ({poster_row['year']})",
            width=220
        )

    st.caption(
        "Ratings and votes are from the downloaded IMDb-based dataset. "
        "Availability of poster images depends on the source URLs."
    )
    
# -------- ADVANCED DATA INSIGHTS --------

st.markdown("---")
st.header("📈 Advanced Data Insights")
st.write(
    "Explore patterns in movie ratings, genre performance, "
    "release decades, and audience engagement."
)

# Prepare separate copies of each dataset
insight_movies = df.copy()
insight_indian = indian_df.copy()

for data in [insight_movies, insight_indian]:
    data["rating"] = pd.to_numeric(data["rating"], errors="coerce")
    data["votes"] = pd.to_numeric(
        data["votes"], errors="coerce"
    ).fillna(0)
    data["year"] = pd.to_numeric(data["year"], errors="coerce")

insight_movies = insight_movies.dropna(subset=["rating", "title"])
insight_indian = insight_indian.dropna(subset=["rating", "title"])

# Dataset selector
insight_source = st.radio(
    "Choose a dataset to analyse",
    ["All MovieLens movies", "Indian / Bollywood movies"],
    horizontal=True,
    key="insight_source"
)

if insight_source == "Indian / Bollywood movies":
    analysis_df = insight_indian.copy()
    analysis_genres = "indian"
    source_label = "Indian / Bollywood"
else:
    analysis_df = insight_movies.copy()
    analysis_genres = "movielens"
    source_label = "MovieLens"

if analysis_df.empty:
    st.warning("There is no data available for this analysis.")
else:
    # Summary metrics
    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("🎬 Movies", f"{len(analysis_df):,}")

    with metric2:
        st.metric(
            "⭐ Average rating",
            f"{analysis_df['rating'].mean():.2f}/10"
        )

    with metric3:
        st.metric(
            "👥 Total recorded votes",
            f"{analysis_df['votes'].sum():,.0f}"
        )

    # Rating distribution
    st.subheader("⭐ Movie Rating Distribution")

    rating_bins = [0, 2, 4, 6, 8, 10]
    rating_labels = [
        "0–2", "2–4", "4–6", "6–8", "8–10"
    ]

    rating_groups = pd.cut(
        analysis_df["rating"],
        bins=rating_bins,
        labels=rating_labels,
        include_lowest=True
    )

    rating_counts = (
        rating_groups.value_counts(sort=False)
        .reindex(rating_labels, fill_value=0)
    )

    st.bar_chart(
        rating_counts.rename_axis("Rating range"),
        x_label="Rating range",
        y_label="Number of movies"
    )

    # Genre analysis
    st.subheader("🎭 Genre Performance")

    if analysis_genres == "indian":
        genre_rows = analysis_df[
            ["title", "genre", "rating", "votes"]
        ].copy()

        genre_rows["genre"] = genre_rows["genre"].fillna("Unknown")
        genre_rows["genre"] = genre_rows["genre"].astype(str).str.split("|")
        genre_rows = genre_rows.explode("genre")
        genre_rows["genre"] = genre_rows["genre"].str.strip()
    else:
        # genre_data already contains one row per movie-genre pair
        genre_rows = genre_data[
            ["title", "genre", "rating", "votes"]
        ].copy()
        genre_rows["rating"] = pd.to_numeric(
            genre_rows["rating"], errors="coerce"
        )
        genre_rows["votes"] = pd.to_numeric(
            genre_rows["votes"], errors="coerce"
        ).fillna(0)

    genre_rows = genre_rows.dropna(subset=["rating", "genre"])
    genre_rows["genre"] = genre_rows["genre"].astype(str).str.strip()
    genre_rows = genre_rows[
        ~genre_rows["genre"].str.lower().isin(
            ["unknown", "nan", "(no genres listed)", ""]
        )
    ]

    genre_summary = (
        genre_rows.groupby("genre")
        .agg(
            movie_count=("title", "nunique"),
            average_rating=("rating", "mean"),
            total_votes=("votes", "sum")
        )
        .sort_values("movie_count", ascending=False)
    )

    if not genre_summary.empty:
        genre_col1, genre_col2 = st.columns(2)

        with genre_col1:
            st.markdown("**Genres with the most movies**")
            st.bar_chart(
                genre_summary.head(10)["movie_count"],
                x_label="Genre",
                y_label="Number of movies"
            )

        with genre_col2:
            # Only show genres with at least 5 movies
            reliable_genres = genre_summary[
                genre_summary["movie_count"] >= 5
            ].sort_values("average_rating", ascending=False)

            st.markdown("**Highest average-rated genres**")

            if reliable_genres.empty:
                st.info("Not enough movies to compare genre averages.")
            else:
                st.bar_chart(
                    reliable_genres.head(10)["average_rating"],
                    x_label="Genre",
                    y_label="Average rating out of 10"
                )

        st.dataframe(
            genre_summary.reset_index().rename(columns={
                "genre": "Genre",
                "movie_count": "Movie count",
                "average_rating": "Average rating",
                "total_votes": "Recorded votes"
            }).round(2),
            width="stretch",
            hide_index=True
        ,
)

    # Release trends by decade
    st.subheader("📅 Movie Releases by Decade")

    decade_df = analysis_df.dropna(subset=["year"]).copy()
    decade_df["Decade"] = (
        (decade_df["year"].astype(int) // 10) * 10
    ).astype(str) + "s"

    decade_counts = (
        decade_df.groupby("Decade")["title"]
        .nunique()
        .sort_index()
    )

    if not decade_counts.empty:
        st.bar_chart(
            decade_counts,
            x_label="Release decade",
            y_label="Number of movies"
        )
    else:
        st.info("Release-year data is unavailable.")

    # Automatic observations
    st.subheader("💡 Automatic Data Insights")

    highest_rated = analysis_df.sort_values(
        ["rating", "votes"], ascending=[False, False]
    ).iloc[0]

    st.write(
        f"🏆 **Highest-rated movie in this dataset:** "
        f"{highest_rated['title']} "
        f"({highest_rated['rating']:.1f}/10)."
    )

    if not genre_summary.empty:
        most_common_genre = genre_summary["movie_count"].idxmax()
        st.write(
            f"🎭 **Most represented genre:** {most_common_genre}, "
            f"with {int(genre_summary.loc[most_common_genre, 'movie_count']):,} "
            "movies."
        )

    if not decade_counts.empty:
        busiest_decade = decade_counts.idxmax()
        st.write(
            f"📅 **Most represented release decade:** {busiest_decade}, "
            f"with {int(decade_counts.max()):,} movies."
        )

    st.caption(
        "These observations describe the loaded datasets, not the entire "
        "global film industry. Average ratings may be less reliable when "
        "based on few votes."
    )

# -------- INDIAN VS MOVIELENS COMPARISON --------

st.markdown("---")
st.header("🌍 Indian Cinema vs MovieLens")
st.write(
    "Compare the datasets' coverage, recorded ratings, and audience votes. "
    "Remember that they come from different sources."
)

compare_col1, compare_col2 = st.columns(2)

with compare_col1:
    st.markdown("### 🇮🇳 Indian / Bollywood")
    st.metric("Movies", f"{len(insight_indian):,}")
    st.metric(
        "Average IMDb rating",
        f"{insight_indian['rating'].mean():.2f}/10"
        if not insight_indian.empty else "N/A"
    )

with compare_col2:
    st.markdown("### 🎞️ MovieLens")
    st.metric("Movies", f"{len(insight_movies):,}")
    st.metric(
        "Average converted rating",
        f"{insight_movies['rating'].mean():.2f}/10"
        if not insight_movies.empty else "N/A"
    )

comparison_table = pd.DataFrame({
    "Dataset": ["Indian / Bollywood", "MovieLens"],
    "Movies": [len(insight_indian), len(insight_movies)],
    "Average rating / 10": [
        insight_indian["rating"].mean(),
        insight_movies["rating"].mean()
    ],
    "Total recorded votes": [
        insight_indian["votes"].sum(),
        insight_movies["votes"].sum()
    ]
})

st.dataframe(
    comparison_table.round(2),
    width="stretch",
    hide_index=True
,
)

st.info(
    "Interpretation: the Indian dataset uses IMDb ratings, while MovieLens "
    "ratings are converted from their original 0.5–5 scale to 1–10. "
    "These are different rating populations, so their averages should not "
    "be treated as a direct, scientifically controlled comparison."
)

# ---------------- GENRE EXPLORER ----------------

st.divider()
st.subheader("🔍 Genre Explorer")

if selected_genre == "All Genres":
    st.info(
        "Choose a specific genre in the sidebar to explore its statistics."
    )
else:
    selected_data = eligible_genres[
        eligible_genres["genre"] == selected_genre
    ].copy()

    if not selected_data.empty:
        best_movie = selected_data.sort_values(
            ["rating", "votes"],
            ascending=[False, False]
        ).iloc[0]

        a, b, c = st.columns(3)

        a.metric(
            "Movies in Genre",
            f"{selected_data['movieId'].nunique():,}"
        )
        b.metric(
            "Genre Average",
            f"{selected_data['rating'].mean():.2f}/10"
        )
        c.metric(
            "Highest-Rated Movie",
            best_movie["title"]
        )

        st.write(
            f"**{selected_genre} insight:** "
            f"The average rating is "
            f"{selected_data['rating'].mean():.2f}/10, "
            f"across {selected_data['movieId'].nunique():,} "
            f"unique movie(s) matching the rating filter."
        )


# ---------------- AUTOMATIC INSIGHTS ----------------

st.divider()
st.subheader("💡 Automatic Data Insights")

if filtered.empty:
    st.info("No movies match the current filters.")
else:
    best = filtered.sort_values(
        ["rating", "votes"],
        ascending=[False, False]
    ).iloc[0]

    st.write(
        f"⭐ The highest-rated movie in the current results is "
        f"**{best['title']}** ({best['rating']:.2f}/10)."
    )

    # Count unique movies for each genre among the filtered movies
    filtered_titles = set(filtered["title"].tolist())

    insight_genres = genre_data[
        (genre_data["title"].isin(filtered_titles))
        & (genre_data["rating"] >= min_rating)
    ]

    if not insight_genres.empty:
        popular_counts = (
            insight_genres.groupby("genre")["movieId"]
            .nunique()
            .sort_values(ascending=False)
        )

        if not popular_counts.empty:
            popular_genre = popular_counts.index[0]
            popular_count = int(popular_counts.iloc[0])

            st.write(
                f"🎭 **{popular_genre}** is the most represented genre "
                f"in the current results, with {popular_count:,} movies."
            )


# ---------------- DOWNLOAD CENTRE ----------------

st.markdown("---")
st.header("📥 MovieScope Download Centre")
st.write(
    "Download movie datasets and analysis results for offline use."
)

download_tab1, download_tab2, download_tab3 = st.tabs([
    "🎬 MovieLens Data",
    "🇮🇳 Indian Movies",
    "🎭 Genre Analysis"
])

with download_tab1:
    st.subheader("Download filtered MovieLens movies")

    st.caption(
        f"Current dashboard filters match {len(filtered):,} movies."
    )

    movielens_csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download filtered MovieLens CSV",
        data=movielens_csv,
        file_name="moviescope_filtered_movies.csv",
        mime="text/csv",
        key="download_movielens"
    )

with download_tab2:
    st.subheader("Download Indian movie data")

    st.caption(
        f"The Indian movie dataset contains {len(indian_df):,} records."
    )

    indian_csv = indian_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="🇮🇳 Download Indian Movies CSV",
        data=indian_csv,
        file_name="moviescope_indian_movies.csv",
        mime="text/csv",
        key="download_indian"
    )

with download_tab3:
    st.subheader("Download genre analysis")

    download_genres = genre_data.copy()

    genre_summary_download = (
        download_genres.groupby("genre")
        .agg(
            movie_count=("movieId", "nunique"),
            average_rating=("rating", "mean"),
            total_votes=("votes", "sum")
        )
        .reset_index()
        .sort_values("movie_count", ascending=False)
    )

    st.dataframe(
        genre_summary_download.round(2),
        width="stretch",
        hide_index=True
    ,
)

    genre_csv = genre_summary_download.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="📊 Download Genre Analysis CSV",
        data=genre_csv,
        file_name="moviescope_genre_analysis.csv",
        mime="text/csv",
        key="download_genres"
    )
    
# ---------------- MOVIE WATCHLIST ----------------

st.markdown("---")
st.header("❤️ My Movie Watchlist")
st.write(
    "Save movies you want to watch. Your watchlist stays available "
    "during the current Streamlit session."
)

# Create the watchlist for the current session
if "movie_watchlist" not in st.session_state:
    st.session_state.movie_watchlist = []

# Combine movie choices from both datasets
watchlist_options = []

for _, movie in df.iterrows():
    watchlist_options.append({
        "title": str(movie["title"]),
        "rating": movie["rating"],
        "year": movie["year"],
        "genre": movie["genre"],
        "source": "MovieLens"
    })

for _, movie in indian_df.iterrows():
    watchlist_options.append({
        "title": str(movie["title"]),
        "rating": movie["rating"],
        "year": movie["year"],
        "genre": movie["genre"],
        "source": "Bollywood (IMDb)"
    })

watchlist_df = pd.DataFrame(watchlist_options)

# Unique labels allow similarly named movies from different datasets
watchlist_df["choice"] = (
    watchlist_df["title"] + " — " + watchlist_df["source"]
)

watchlist_df = watchlist_df.drop_duplicates(subset=["choice"])

if not watchlist_df.empty:
    chosen_movie = st.selectbox(
        "🎬 Choose a movie to save",
        watchlist_df["choice"].tolist(),
        key="watchlist_movie_choice"
    )

    if st.button("❤️ Add to Watchlist", key="add_watchlist_movie"):
        selected_row = watchlist_df[
            watchlist_df["choice"] == chosen_movie
        ].iloc[0]

        saved_movie = {
            "choice": selected_row["choice"],
            "title": selected_row["title"],
            "rating": selected_row["rating"],
            "year": selected_row["year"],
            "genre": selected_row["genre"],
            "source": selected_row["source"]
        }

        if not any(
            item["choice"] == saved_movie["choice"]
            for item in st.session_state.movie_watchlist
        ):
            st.session_state.movie_watchlist.append(saved_movie)
            st.success(f"🎉 {saved_movie['title']} added to your watchlist!")
        else:
            st.info("This movie is already in your watchlist.")

# Display saved movies
st.subheader(
    f"📋 Saved Movies ({len(st.session_state.movie_watchlist)})"
)

if st.session_state.movie_watchlist:
    saved_df = pd.DataFrame(st.session_state.movie_watchlist)

    st.dataframe(
        saved_df[["title", "year", "genre", "rating", "source"]],
        width="stretch",
        hide_index=True
    ,
)

    remove_choice = st.selectbox(
        "Select a movie to remove",
        [movie["choice"] for movie in st.session_state.movie_watchlist],
        key="remove_watchlist_choice"
    )

    if st.button("🗑️ Remove Selected Movie", key="remove_watchlist_movie"):
        st.session_state.movie_watchlist = [
            movie for movie in st.session_state.movie_watchlist
            if movie["choice"] != remove_choice
        ]
        st.rerun()

    watchlist_csv = saved_df[
        ["title", "year", "genre", "rating", "source"]
    ].to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download My Watchlist",
        data=watchlist_csv,
        file_name="moviescope_watchlist.csv",
        mime="text/csv",
        key="download_watchlist"
    )
else:
    st.info(
        "Your watchlist is empty. Choose a movie above and click "
        "'Add to Watchlist' to save your first movie."
    )

st.caption(
    "Watchlist items are stored in the current session and may be lost "
    "when the session resets or the app restarts."
)



# ---------------- FULL DATASET ----------------

with st.expander("📁 View Filtered Dataset"):
    st.dataframe(
        filtered,
        width="stretch",
        hide_index=True
    ,
)

st.caption(
    "MovieScope | Fundamentals of Data Science Mini Project | "
    "Source: GroupLens MovieLens Small dataset"
)
