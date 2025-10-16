import sys


def load_movies_file(filename):
    """
    Given a movies file, return dictionary of movies in the following format:
    {'movie name': ('genre', 'id')}
    """
    movies = {}
    with open(filename, "r") as f:
        for line in f:
            genre, movie_id, name = line.strip().split("|")
            movies[name] = genre, movie_id
    print(f"Loaded {len(movies)} movies from {filename}")
    return movies


def load_ratings_file(filename):
    """
    Given a ratings file, return dictionary of ratings in the following format:
    {'movie name': [('rating1', 'id1'), ('rating2', 'id2')]}
    """
    ratings = {}
    with open(filename, "r") as f:
        for line in f:
            name, rating, user_id = line.strip().split("|")
            ratings.setdefault(name, []).append((float(rating), int(user_id)))
    print(f"Loaded {len(ratings)} ratings from {filename}...")
    return ratings


def movie_popularity(ratings, n):
    """
    Calculate and display the top N movies ranked by their average rating.

    Each movie's average rating is calculated by taking the mean of all its user ratings.
    The movies are then sorted in descending order of their average rating, and the top N
    movies are printed.
    """
    averages = {}
    for movie in ratings:
        just_ratings = [r for r, u in ratings[movie]]
        avg = sum(just_ratings) / len(just_ratings)
        averages[movie] = avg
    sorted_averages = dict(
        sorted(averages.items(), key=lambda item: item[1], reverse=True)
    )
    sorted_movies = list(sorted_averages.keys())
    print("\n")
    print(f"Here are the top {n} movies:")
    for i in range(n):
        print(sorted_movies[i])


def movie_popularity_in_genre(movies, ratings, genre, n):
    """
    Calculate and display the top N movies within a specific genre ranked by their average rating.

    For all movies that belong to the specified genre, their average ratings are calculated 
    based on user ratings. The results are then sorted from highest to lowest average rating, 
    and the top N movies are printed.
    """
    movie_scores = {}
    for movie_name, (movie_genre, movie_id) in movies.items():
        if movie_genre.lower() == genre.lower():
            if movie_name in ratings:
                scores = [r for r, _ in ratings[movie_name]]
                avg = sum(scores) / len(scores)
                movie_scores[movie_name] = avg
    sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_movies[:n]
    print(f"\nTop {n} {genre} movies (by average rating):")
    for movie, avg in top_n:
        print(f"{movie}: {avg:.2f}")

def genre_popularity(movies, ratings, n):
    """
    Calculate and return the top N genres by average movie rating (case-insensitive).

    Movie names and genres are treated in a case-insensitive way. 
    For example, "Inception" and "inception" will be considered the same movie,
    and "Sci-Fi" and "sci-fi" will be treated as the same genre.

    Args:
        movies (dict): Dictionary where keys are movie names (any case) and values are tuples/lists.
                       The first element in the tuple/list should be the genre of the movie.
                       Example: {"Inception": ("Sci-Fi", 2010)}
        ratings (dict): Dictionary where keys are movie names (any case) and values are lists of tuples,
                        each containing a rating and a user ID.
                        Example: {"Inception": [(5, 101), (4, 102)]}
        n (int): Number of top genres to return.

    Returns:
        list: List of tuples containing the top N genres (properly capitalized) and their average ratings,
              sorted in descending order by average rating.
              Example: [("Sci-Fi", 4.5), ("Drama", 4.2)]

    Prints:
        Top N genres by average rating with two decimal places.
    """

    # Normalize movie names and genres to lowercase for matching
    movies_lower = {name.lower(): (vals[0].strip().lower(), *vals[1:]) for name, vals in movies.items()}
    ratings_lower = {name.lower(): val for name, val in ratings.items()}

    # Calculate average rating per movie
    movie_avg = {}
    for movie_name, rating_list in ratings_lower.items():
        avg = sum(r for r, _ in rating_list) / len(rating_list)
        movie_avg[movie_name] = avg

    # Aggregate ratings by genre
    genre_totals = {}
    genre_counts = {}
    for movie_name, avg in movie_avg.items():
        if movie_name in movies_lower:
            genre = movies_lower[movie_name][0]
            genre_totals[genre] = genre_totals.get(genre, 0) + avg
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Calculate average rating per genre
    genre_avg = {g: genre_totals[g] / genre_counts[g] for g in genre_totals}
    sorted_genres = sorted(genre_avg.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop {n} genres by average rating:")
    for genre, avg in sorted_genres[:n]:
        print(f"{genre.title()}: {avg:.2f}")

    # Return top N genres with proper capitalization
    return [(genre.title(), avg) for genre, avg in sorted_genres[:n]]

def user_preference(movies, ratings, user_id):
    """
    Determine a user's preferred genre based on their ratings (case-insensitive).

    Movie names and genres are treated in a case-insensitive way. 
    For example, "Inception" and "inception" will be considered the same movie,
    and "Sci-Fi" and "sci-fi" will be treated as the same genre.

    Args:
        movies (dict): Dictionary where keys are movie names (any case) and values are tuples/lists.
                       The first element in the tuple/list should be the genre of the movie.
                       Example: {"Inception": ("Sci-Fi", 2010)}
        ratings (dict): Dictionary where keys are movie names (any case) and values are lists of tuples,
                        each containing a rating and a user ID.
                        Example: {"Inception": [(5, 101), (4, 102)]}
        user_id (int): The ID of the user whose preferred genre is being calculated.

    Returns:
        str or None: The genre that the user has rated highest on average. 
                     Returns None if the user has not rated any movies.

    Prints:
        The user's preferred genre along with its average rating.
    """

    # Normalize movie names and genres to lowercase for matching
    movies_lower = {name.lower(): (vals[0].strip().lower(), *vals[1:]) for name, vals in movies.items()}
    ratings_lower = {name.lower(): val for name, val in ratings.items()}

    genre_totals = {}
    genre_counts = {}

    for movie_name, rating_list in ratings_lower.items():
        if movie_name not in movies_lower:
            continue

        # Find ratings by this specific user
        user_ratings = [r for r, uid in rating_list if uid == user_id]

        if user_ratings:
            avg_user_rating = sum(user_ratings) / len(user_ratings)
            genre = movies_lower[movie_name][0]
            genre_totals[genre] = genre_totals.get(genre, 0) + avg_user_rating
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    if not genre_totals:
        print(f"User {user_id} has not rated any movies in the database.")
        return None

    # Calculate average rating per genre for this user
    genre_avg = {g: genre_totals[g] / genre_counts[g] for g in genre_totals}
    preferred_genre = max(genre_avg.items(), key=lambda x: x[1])[0]

    print(f"User {user_id}'s preferred genre is: {preferred_genre.title()} "
          f"(average rating: {genre_avg[preferred_genre]:.2f})")

    return preferred_genre.title()

def recommend_movies(user_id, movies, ratings):
    """
    Recommend 3 most popular movies from the user's top genre
    that the user has not yet rated.
    """
    if not movies or not ratings:
        print("Please load movies and ratings data first.")
        return

    preferred_genre = user_preference(movies, ratings, int(user_id))
    if not preferred_genre:
        print("Cannot determine preferred genre — user may not have rated any movies.")
        return

    genre_movies = {
        name: (genre, mid)
        for name, (genre, mid) in movies.items()
        if genre.lower() == preferred_genre.lower()
    }
    rated_movies = set()
    for movie_name, rating_list in ratings.items():
        for _, uid in rating_list:
            if uid == int(user_id):
                rated_movies.add(movie_name)

    movie_scores = {}
    for movie_name, (genre, mid) in genre_movies.items():
        if movie_name not in rated_movies and movie_name in ratings:
            scores = [r for r, _ in ratings[movie_name]]
            avg = sum(scores) / len(scores)
            movie_scores[movie_name] = avg

    sorted_recs = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    print(f"\nTop 3 recommended movies for User {user_id} (Genre: {preferred_genre}):")
    if not sorted_recs:
        print("No unrated movies available in your top genre.")
        return

    for movie, avg in sorted_recs[:3]:
        print(f"{movie}: {avg:.2f}")


def print_menu():
    print("\n=== Movie Recommender Menu ===")
    print("1. Load movie data file")
    print("2. Load ratings data file")
    print("3. Show top N movies")
    print("4. Show top N movies in a genre")
    print("5. Show top N genres")
    print("6. Show user's top genre")
    print("7. Recommend movies for a user")
    print("8. Exit")


def main():
    """
    Main interactive menu loop for the movie recommender system.
    Allows the user to load data files and test various functions interactively.
    """
    movies = []
    ratings = []

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                filename = input("Enter movie data filename: ").strip()
                movies = load_movies_file(filename)
            except FileNotFoundError:
                print("Error: File not found.")
            except Exception as e:
                print(f"Unexpected error loading movies file: {e}")

        elif choice == "2":
            try:
                filename = input("Enter ratings data filename: ").strip()
                ratings = load_ratings_file(filename)
            except FileNotFoundError:
                print("Error: File not found.")
            except Exception as e:
                print(f"Unexpected error loading ratings file: {e}")

        elif choice == "3":
            try:
                n = int(input("Enter N: ").strip())
                movie_popularity(ratings, n)
            except ValueError:
                print("Invalid input. Please enter an integer for N.")
            except Exception as e:
                print(f"Error running movie popularity: {e}")

        elif choice == "4":
            try:
                genre = input("Enter genre: ").strip()
                n = int(input("Enter N: ").strip())
                movie_popularity_in_genre(movies, ratings, genre, n)
            except ValueError:
                print("Invalid input. Please enter an integer for N.")
            except Exception as e:
                print(f"Error running movie popularity in genre: {e}")

        elif choice == "5":
            try:
                n = int(input("Enter N: ").strip())
                genre_popularity(movies, ratings, n)
            except ValueError:
                print("Invalid input. Please enter an integer for N.")
            except Exception as e:
                print(f"Error running genre popularity: {e}")

        elif choice == "6":
            try:
                user_id = int(input("Enter user ID: ").strip())
                user_preference(movies, ratings, user_id)
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except Exception as e:
                print(f"Error running user preference: {e}")

        elif choice == "7":
            try:
                user_id = int(input("Enter user ID: ").strip())
                recommend_movies(user_id, movies, ratings)
            except ValueError:
                print("Invalid input. Please enter an integer for user ID.")
            except Exception as e:
                print(f"Error running movie recommendation: {e}")

        elif choice == "8":
            print("Exiting program.")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
