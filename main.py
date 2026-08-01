from src.services.library_service import LibraryService

def main():
    library = LibraryService()

    while True:
        print("\n===== Library Management System =====")
        print("1. Add Book")
        print("2. Show All Books")
        print("3. Add Member")
        print("4. Show Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Show Activity Log")
        print("8. Undo Last Action")
        print("9. Redo Last Action")
        print("10. Reports")
        print("11. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            title = input("Enter title: ")
            author = input("Enter author: ")
            library.add_book(title, author)

        elif choice == "2":
            library.show_books()

        elif choice == "3":
            name = input("Member name: ")
            email = input("Member email: ")
            library.add_member(name, email)

        elif choice == "4":
            library.show_members()

        elif choice == "5":
            book_id = int(input("Book ID to borrow: "))
            member_id = int(input("Member ID: "))
            library.request_borrow(book_id, member_id)

        elif choice == "6":
            transaction_id = int(input("Transaction ID to return: "))
            library.return_book(transaction_id)

        elif choice == "7":
            library.print_activity()

        elif choice == "8":
            library.undo()

        elif choice == "9":
            library.redo()

        elif choice == "10":
            library.generate_reports()

        elif choice == "11":
            print("Goodbye!")
            break

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
