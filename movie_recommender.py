import sys

def load_movies_file(filename):
    movies = {}
    with open(filename, "r") as f:
        for line in f:
            genre, movie_id, name = line.strip().split('|')
            movies[name] = genre
    print(f"Loaded {len(movies)} movies from {filename}")
    return movies

def load_ratings_file(filename):
    ratings = {}
    with open(filename, "r") as f:
        for line in f:
            name, rating, user_id = line.strip().split('|')
            ratings.setdefault(name, []).append((float(rating), int(user_id)))
    print(f"Loaded {len(ratings)} ratings from {filename}...")
    return ratings

def movie_popularity(ratings, n):
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
    

'''
def movie_popularity_in_genre(int: n):

def genre_popularity(int: n):

def user_preference():

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
            user_id = input("Enter user ID: ").strip()
            user_preference(user_id, movies, ratings)

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
