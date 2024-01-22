import database
import random
import string


def generate_books(number_of_books):

    words = ["Secrets", "Legacy", "Journey", "Dreams", "Chronicles", "Empire", "Shadow", "Fortune", "Quest", "Heart"]

    first_names = ["John", "Jane", "Alice", "Mark", "Chloe", "Derek", "Laura", "Luke"]
    last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Wilson"]

    genres = ["Fiction", "Non-Fiction", "Mystery", "Science Fiction", "Fantasy", "Biography", "Romance", "History"]

    for _ in range(number_of_books):
        isbn = ''.join(random.choices(string.digits, k=13))
        title = "The " + " ".join(random.choice(words) for _ in range(3))
        author = random.choice(first_names) + " " + random.choice(last_names)
        genre = random.choice(genres)
        quantity = random.randint(1, 10)
        database.add_book(isbn, title, author, genre, quantity)


def add_users(number_of_users):

    first_names = ["John", "Jane", "Alice", "Mark", "Chloe", "Derek", "Laura", "Luke"]
    last_names = ["Smith", "Johnson", "Brown", "Williams", "Jones", "Miller", "Davis", "Wilson"]

    for _ in range(number_of_users):
        student_id = ''.join(random.choices(string.digits, k=8))
        name = random.choice(first_names) + " " + random.choice(last_names)
        database.add_user(student_id, name)


def simulate_borrowing(number_of_borrows):
    all_books = database.list_all_books()
    all_users = database.list_all_users()

    for _ in range(number_of_borrows):
        random_book = random.choice(all_books)
        random_user = random.choice(all_users)
        database.borrow_book(random_user[0], random_book[0])


def main():
    print("Setting up the database...")
    database.setupDatabase()

    print("\nGenerating and adding 100 books...")
    generate_books(100)

    print("\nAdding 50 users...")
    add_users(50)

    print("\nSimulating 20 book borrowing...")
    simulate_borrowing(20)


if __name__ == "__main__":
    main()
