import sys

def load_movies_file(filename):
    print(f"Loading movies from {filename}...")
    return []

def load_ratings_file(filename):
    print(f"Loading ratings from {filename}...")
    return []

'''
def movie_popularity(int: n):
    
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
            top_n_movies(movies, ratings, n)

        elif choice == "4":
            genre = input("Enter genre: ").strip()
            n = int(input("Enter N: ").strip())
            top_n_movies_in_genre(movies, ratings, genre, n)

        elif choice == "5":
            n = int(input("Enter N: ").strip())
            top_n_genres(movies, ratings, n)

        elif choice == "6":
            user_id = input("Enter user ID: ").strip()
            user_top_genre(user_id, movies, ratings)

        elif choice == "7":
            user_id = input("Enter user ID: ").strip()
            recommend_movies(user_id, movies, ratings)

        elif choice == "8":
            print("Exiting program. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
