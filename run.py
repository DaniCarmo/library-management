"""
Import libraries/ packages.
"""
import os
import sys
from termcolor import colored
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

# Error handling if json file not found
try:
    CREDS = Credentials.from_service_account_file('creds.json')
except FileNotFoundError as e:
    print(f"Error: 'creds.json' file not found. Make sure the file exists.")

SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('book_repository')


def load_books():
    """
    Load all books in the spreadsheet.
    """
    global numberOfBooks
    clear_screen()
    print("Please wait while books are being loaded...")
    print("Done loading books.\n")

    # Handle error if spreadsheet cannot load
    try:
        booklist = SHEET.worksheet('books')
        data = booklist.get_all_values()
    except gspread.exceptions.APIError as e:
        print(f"An error occurred while accessing Google Sheets: {e}")

    # Extract the data rows and get total no of books
    all_data = data[1:]
    numberOfBooks = len(all_data)

    # Create dictionaries of results
    book_info = {}
    for row in all_data:
        title, publisher, subject = row
        book_info[title] = {'publisher': publisher, 'subject': subject}

    return book_info


def search_by_field(books, search_field, search_term):
    """
    Search for books by specific field (title, publisher, subject).
    """
    matching_books = {}
    for title, info in books.items():
        if search_term.lower() in info[search_field].lower():
            matching_books[title] = info

    return matching_books


def checkout_message(book_title):
    """
    Message to appear to user upon checking out
    """
    clear_screen()
    print(f"Great! You have successfully checked out '{book_title}'.")
    print("Please collect it from the library reception by 3pm today.")
    print("Enjoy your reading!")


def main():
    """
    Start the program and runs until user exits
    """
    books = load_books()

    while True:
        clear_screen()
        print("Welcome to Your Leaving Cert Library!")
        print(f"There are currently {len(books)} books in the library.")
        print("To find and check out a book, please select an option below:")
        print("(1) Search by Subject")
        print("(2) Search by Publisher")
        print("(3) Search by Title")

        user_choice = input("Enter your choice (1/2/3): ")

        if not user_choice:
            print("Sorry you must enter an option above to continue!")
            continue

        if user_choice == "1":
            search_term = input("Please enter the subject: ")
            matching_books = search_by_field(books, 'subject', search_term)
        elif user_choice == "2":
            search_term = input("Please enter the publisher: ")
            matching_books = search_by_field(books, 'publisher', search_term)
        elif user_choice == "3":
            search_term = input("Please enter the title: ")
            matching_books = search_by_field(books, 'title', search_term)
        else:
            print("Oops! Please choose option 1, 2, or 3.")
            continue

        if not matching_books:
            print(f'Uh oh! No matching books found for "{search_term}".')

        for title in matching_books:
            print(f'Title: {title}')
            print(f'Publisher: {matching_books[title]["publisher"]}')
            print(f'Subject: {matching_books[title]["subject"]}')

        checkout_book = input("Enter book title to check out or 'q' to quit:")
      
        if checkout_book.lower() == 'q':
            break

        if checkout_book in matching_books:
            clear_screen()
            checkout_message(checkout_book)
        else:
            print("Looks like our library does not have that book.\n")
            print("Let's see if we can help find what you're looking for!\n")
            print("Returning to search menu....")


def clear_screen():
    """
    Clear the terminal screen.
    """
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')


if __name__ == "__main__":
    main()
