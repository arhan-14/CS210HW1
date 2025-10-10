import sys

def load_movies_file(filename):
    """
    Given a movies file, return dictionary of movies in the following format:
    {'movie name': ('genre', 'id')}
    """
    movies = {}
    with open(filename, "r") as f:
        for line in f:
            genre, movie_id, name = line.strip().split('|')
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
            name, rating, user_id = line.strip().split('|')
            ratings.setdefault(name, []).append((float(rating), int(user_id)))
    print(f"Loaded {len(ratings)} ratings from {filename}...")
    return ratings

def movie_popularity(ratings, n):
    print(f"{ratings}")
    averages = {}
    for movie in ratings:
        just_ratings = [r for r, u in ratings[movie]]
        avg = sum(just_ratings)/len(just_ratings)
        averages[movie] = avg
    sorted_averages = dict(sorted(averages.items(), key=lambda item: item[1], reverse=True))
    sorted_movies = list(sorted_averages.keys())
    print('\n')
    print(f"Here are the top {n} movies:")
    for i in range(n):
        print(sorted_movies[i])
    
def movie_popularity_in_genre(movies, ratings, genre, n):
    movie_scores = {}
    for movie_name, (movie_genre, movie_id) in movies.items():
        if movie_genre.lower() == genre.lower():
            if movie_name in ratings:
                scores = [r for r, _ in ratings[movie_name]]
                avg = sum(scores)/len(scores)
                movie_scores[movie_name] = avg
    sorted_movies = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_movies[:n]
    print(f"\nTop {n} {genre} movies (by average rating):")
    for movie, avg in top_n:
        print(f"{movie}: {avg:.2f}")


def genre_popularity(movies, ratings, n):
    movie_avg = {}
    for movie_name, rating_list in ratings.items():
        avg = sum(r for r, _ in rating_list) / len(rating_list)
        movie_avg[movie_name] = avg

    genre_totals = {} 
    genre_counts = {}  
    for movie_name, avg in movie_avg.items():
        if movie_name in movies:
            genre = movies[movie_name][0] 
            genre_totals[genre] = genre_totals.get(genre, 0) + avg
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    genre_avg = {}
    for genre in genre_totals:
        genre_avg[genre] = genre_totals[genre] / genre_counts[genre]

    sorted_genres = sorted(genre_avg.items(), key=lambda x: x[1], reverse=True)

    print(f"\nTop {n} genres by average rating:")
    for genre, avg in sorted_genres[:n]:
        print(f"{genre}: {avg:.2f}")

    return sorted_genres[:n]

def user_preference(movies, ratings, user_id):
    genre_totals = {} 
    genre_counts = {} 

    for movie_name, rating_list in ratings.items():
        movie_name_clean = movie_name.strip() 

        
        if movie_name_clean not in movies:
            continue

       
        user_ratings = [r for r, uid in rating_list if uid == user_id]

        if user_ratings:
            avg_user_rating = sum(user_ratings) / len(user_ratings)
            genre = movies[movie_name_clean][0].strip()  
            genre_totals[genre] = genre_totals.get(genre, 0) + avg_user_rating
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    if not genre_totals:
        print(f"User {user_id} has not rated any movies in the database.")
        return None

    
    genre_avg = {genre: genre_totals[genre] / genre_counts[genre] for genre in genre_totals}

    
    preferred_genre = max(genre_avg.items(), key=lambda x: x[1])[0]

    print(f"User {user_id}'s preferred genre is: {preferred_genre} "
          f"(average rating: {genre_avg[preferred_genre]:.2f})")

    return preferred_genre



'''
def recommend_movies():
'''

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
    movies = []
    ratings = []

    while True:
        print_menu()
        choice = input("Enter choice: ").strip()

        if choice == "1":
            filename = input("Enter movie data filename: ").strip()
            movies = load_movies_file(filename)

        elif choice == "2":
            filename = input("Enter ratings data filename: ").strip()
            ratings = load_ratings_file(filename)

        elif choice == "3":
            n = int(input("Enter N: ").strip())
            movie_popularity(ratings, n)

        elif choice == "4":
            genre = input("Enter genre: ").strip()
            n = int(input("Enter N: ").strip())
            movie_popularity_in_genre(movies, ratings, genre, n)

        elif choice == "5":
            n = int(input("Enter N: ").strip())
            genre_popularity(movies, ratings, n)

        elif choice == "6":
            user_id = int(input("Enter user id: "))
            user_preference(movies, ratings, user_id)


        elif choice == "7":
            user_id = input("Enter user ID: ").strip()
            recommend_movies(user_id, movies, ratings)

        elif choice == "8":
            print("Exiting program.")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()