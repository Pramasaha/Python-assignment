import sys

class DuplicateISBNError(Exception):
    pass

class DuplicateMemberIDError(Exception):

    pass

class BookNotFoundError(Exception):
 
    pass

class MemberNotFoundError(Exception):

    pass

class BookUnavailableError(Exception):

    pass

class BookAlreadyBorrowedError(Exception):

    pass

class InvalidAgeError(Exception):

    pass

class EmptyInputError(Exception):

    pass



class Person:

    
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def display_info(self):

        print(f"Name : {self.name}")
        print(f"Age : {self.age}")


class Book:

    

    total_books = 0
    
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.__available = True 
        self.isbn = isbn
        Book.total_books += 1 
    
    @property
    def available(self):
   
        return self.__available
    
    @available.setter
    def available(self, status):
   
        if isinstance(status, bool):
            self.__available = status
        else:
            raise ValueError("Availability must be a boolean value")
    
    @property
    def status(self):
        return 'Available' if self.__available else 'Borrowed'
    
    @classmethod
    def get_total_books(cls):
        return cls.total_books
    
    @staticmethod
    def format_isbn(isbn):
        return isbn.strip().upper()
    
    @staticmethod
    def validate_title(title):
        return title is not None and title.strip() != ""
    
    @staticmethod
    def validate_author(author):
        return author is not None and author.strip() != ""
    
    def display_book(self):
        print(f"ISBN : {self.isbn}")
        print(f"Title : {self.title}")
        print(f"Author : {self.author}")
        print(f"Status : {self.status}")


class Member(Person):
    
    total_members = 0
    
    def __init__(self, member_id, name, age):
        super().__init__(name, age) 
        self.member_id = member_id
        self.borrowed_books = []    
        Member.total_members += 1 
    
    @classmethod
    def get_total_members(cls):
        return cls.total_members
    
    @staticmethod
    def validate_age(age):
        return age > 0
    
    @staticmethod
    def validate_name(name):
        return name is not None and name.strip() != ""
    
    def borrow_book(self, book):
        self.borrowed_books.append(book)
    
    def return_book(self, book):
        self.borrowed_books.remove(book)
    
    def has_borrowed_book(self, book):
        return book in self.borrowed_books
    
    def display_info(self):
        print(f"Member ID : {self.member_id}")
        super().display_info() 
        print(f"Borrowed Books : {len(self.borrowed_books)}")


class Library:
    def __init__(self):
        self.books = []    
        self.members = [] 
    
    def _find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def _find_member_by_id(self, member_id):
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None
    
    def add_book(self, title, author, isbn):
        if not Book.validate_title(title):
            raise EmptyInputError("Book title cannot be empty.")
        if not Book.validate_author(author):
            raise EmptyInputError("Author name cannot be empty.")
        
        formatted_isbn = Book.format_isbn(isbn)
        
        if self._find_book_by_isbn(formatted_isbn) is not None:
            raise DuplicateISBNError("ISBN already exists.")
        
        new_book = Book(title.strip(), author.strip(), formatted_isbn)
        self.books.append(new_book)
    
    def register_member(self, member_id, name, age):
        if not Member.validate_name(name):
            raise EmptyInputError("Name cannot be empty.")
        if not Member.validate_age(age):
            raise InvalidAgeError("Age must be greater than 0.")
        
        if self._find_member_by_id(member_id.strip()) is not None:
            raise DuplicateMemberIDError("Member ID already exists.")
        
        new_member = Member(member_id.strip(), name.strip(), age)
        self.members.append(new_member)
    
    def borrow_book(self, member_id, isbn):
        member = self._find_member_by_id(member_id.strip())
        if member is None:
            raise MemberNotFoundError("Member not found.")
        
        book = self._find_book_by_isbn(Book.format_isbn(isbn))
        if book is None:
            raise BookNotFoundError("Book not found.")
        
        if not book.available:
            raise BookUnavailableError("Sorry! This book is currently unavailable.")
        
        if member.has_borrowed_book(book):
            raise BookAlreadyBorrowedError("You have already borrowed this book.")
        
        member.borrow_book(book)
        book.available = False
    
    def return_book(self, member_id, isbn):
        member = self._find_member_by_id(member_id.strip())
        if member is None:
            raise MemberNotFoundError("Member not found.")
        
        book = self._find_book_by_isbn(Book.format_isbn(isbn))
        if book is None or not member.has_borrowed_book(book):
            raise BookNotFoundError("Book not found.")
        
        member.return_book(book)
        book.available = True
    
    def show_books(self):
        if not self.books:
            print("No books available in the library.")
            return
        
        print("------------- BOOK LIST -------------")
        for book in self.books:
            book.display_book()
            print("-------------------------------------")
    
    def show_members(self):
        if not self.members:
            print("No members registered in the library.")
            return
        
        print("----------- MEMBER LIST ------------")
        for member in self.members:
            member.display_info()
            print("------------------------------------")
    
    def search_book(self, title):
        for book in self.books:
            if book.title.lower() == title.strip().lower():
                return book
        return None


class LibraryManagementSystem:
    
    def __init__(self):
        self.library = Library()
    
    def display_menu(self):
        print("=========================================")
        print("LIBRARY MANAGEMENT SYSTEM")
        print("=========================================")
        print()
        print("1. Add Book")
        print("2. Register Member")
        print("3. Borrow Book")
        print("4. Return Book")
        print("5. Show All Books")
        print("6. Show All Members")
        print("7. Search Book")
        print("8. Exit")
        print()
    
    def add_book(self):
        print("\n----- Add New Book -----")
        try:
            title = input("Enter Book Title : ").strip()
            author = input("Enter Author : ").strip()
            isbn = input("Enter ISBN : ").strip()
            self.library.add_book(title, author, isbn)
            print("\nBook added successfully!")
        except EmptyInputError as e:
            print(f"\nError: {e}")
        except DuplicateISBNError:
            print("\nError: ISBN already exists.")
        except Exception:
            print("\nError: An unexpected error occurred.")
    
    def register_member(self):
        print("\n----- Register Member -----")
        try:
            member_id = input("Enter Member ID : ").strip()
            name = input("Enter Name : ").strip()
            age_input = input("Enter Age : ").strip()
            
            if not age_input:
                raise EmptyInputError("Age cannot be empty.")
            
            age = int(age_input)
            self.library.register_member(member_id, name, age)
            print("\nMember registered successfully!")
            
        except EmptyInputError as e:
            print(f"\nError: {e}")
        except InvalidAgeError:
            print("\nError: Age must be greater than 0.")
        except ValueError:
            print("\nError: Invalid age input. Please enter a valid number.")
        except DuplicateMemberIDError:
            print("\nError: Member ID already exists.")
        except Exception:
            print("\nError: An unexpected error occurred.")
    
    def borrow_book(self):
        print("\n------ Borrow Book ------")
        try:
            member_id = input("Enter Member ID : ").strip()
            isbn = input("Enter Book ISBN : ").strip()
            self.library.borrow_book(member_id, isbn)
            print("\nBook borrowed successfully.")
        except MemberNotFoundError:
            print("\nMember not found.")
        except BookNotFoundError:
            print("\nBook not found.")
        except BookUnavailableError:
            print("\nSorry! This book is currently unavailable.")
        except BookAlreadyBorrowedError:
            print("\nSorry! You have already borrowed this book.")
        except Exception:
            print("\nError: An unexpected error occurred.")
    
    def return_book(self):
        print("\n------ Return Book ------")
        try:
            member_id = input("Enter Member ID : ").strip()
            isbn = input("Enter Book ISBN : ").strip()
            self.library.return_book(member_id, isbn)
            print("\nBook returned successfully.")
        except MemberNotFoundError:
            print("\nMember not found.")
        except BookNotFoundError:
            print("\nBook not found.")
        except Exception:
            print("\nError: An unexpected error occurred.")
    
    def search_book(self):
        print("\n------ Search Book ------")
        try:
            title = input("Enter Book Title : ").strip()
            if not title:
                raise EmptyInputError("Title cannot be empty.")
            
            book = self.library.search_book(title)
            if book:
                print("\nBook Found!")
                print()
                book.display_book()
            else:
                print("\nBook not found.")
        except EmptyInputError as e:
            print(f"\nError: {e}")
        except Exception:
            print("\nError: An unexpected error occurred.")
    
    def run(self):
        """Main application loop"""
        while True:
            try:
                self.display_menu()
                choice = input("Enter your choice: ").strip()
                
                if choice == "1":
                    self.add_book()
                elif choice == "2":
                    self.register_member()
                elif choice == "3":
                    self.borrow_book()
                elif choice == "4":
                    self.return_book()
                elif choice == "5":
                    print()
                    self.library.show_books()
                elif choice == "6":
                    print()
                    self.library.show_members()
                elif choice == "7":
                    self.search_book()
                elif choice == "8":
                    print("\nThank you for using Library Management System.")
                    print("Goodbye!")
                    sys.exit(0)
                else:
                    print("\nError: Invalid choice. Please enter a number between 1 and 8.")
                
                if choice != "8":
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Exiting...")
                sys.exit(0)
            except Exception:
                print("\nError: An unexpected runtime error occurred.")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()