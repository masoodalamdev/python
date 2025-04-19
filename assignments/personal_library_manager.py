import json
import os

# File to store the library
FILE_NAME = "library.json"

# Load library from file if it exists
def load_library():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    return []

# Save library to file
def save_library(library):
    with open(FILE_NAME, 'w') as file:
        json.dump(library, file, indent=4)

# Add a book
def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    try:
        year = int(input("Enter the publication year: ").strip())
    except ValueError:
        print("❌ Invalid year. Book not added.")
        return
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read_status = True if read_input == "yes" else False

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    }

    library.append(book)
    print("✅ Book added successfully!")

# Remove a book
def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip()
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            print("✅ Book removed successfully!")
            return
    print("❌ Book not found.")

# Search for books
def search_books(library):
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ").strip()
    query = input("Enter the search term: ").strip().lower()

    matches = []
    for book in library:
        if (choice == '1' and query in book["title"].lower()) or \
           (choice == '2' and query in book["author"].lower()):
            matches.append(book)

    if matches:
        print("\n📚 Matching Books:")
        for idx, book in enumerate(matches, 1):
            print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("❌ No matching books found.")

# Display all books
def display_books(library):
    if not library:
        print("📭 Your library is empty.")
        return

    print("\n📚 Your Library:")
    for idx, book in enumerate(library, 1):
        print(f"{idx}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

# Display statistics
def display_statistics(library):
    total = len(library)
    if total == 0:
        print("📊 No books in your library.")
        return

    read_count = sum(book['read'] for book in library)
    percentage = (read_count / total) * 100
    print(f"\n📈 Total books: {total}")
    print(f"✅ Books read: {read_count}")
    print(f"📖 Percentage read: {percentage:.2f}%")

# Main menu loop
def menu():
    library = load_library()
    while True:
        print("\n📘 Welcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_books(library)
        elif choice == '4':
            display_books(library)
        elif choice == '5':
            display_statistics(library)
        elif choice == '6':
            save_library(library)
            print("💾 Library saved. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please try again.")

# Run the app
if __name__ == "__main__":
    menu()
