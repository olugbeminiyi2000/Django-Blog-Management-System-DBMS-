"""
A script that creates a new instance of a book
that takes in four command line arguments to
create the instance;
<author_name> <book_name> <language or no language> <status or no status>

author_name:
    this is created using the Author class
    takes only one argument i.e Author(author=value).
language:
    this created using the Language class
    takes only one argument i.e Language(language=value)
    the values are in the value.choices=["en, "fr", "rw"] any one of
    these values.
status:
    this is created using the Status class
    takes only one argument i.e Status(status=value)
    the values are in the value.choice=["AVL", "ONL", "RES"] any one of
    these values.
book_name:
    this is created using the Book class
    takes three argument i.e Book(book=value,
    author_name=author, language_name=language).
instance:
    this is not taking as an argument but it is created
    inside of this script, it takes a 2 arguements i.e
    Instance(book_name=book, status_name=status).
"""
from bookstores.models import Author, Language, Status, Book, Instance


def run(*args):
    if len(args) == 0:
        print("no argument given, arguments should be in this order\n\
<author_name> <book_name> <language or no language> \
<status or no status>"
        )
        return 1
    elif len(args) < 2:
        print("missing book-name argument, arguments should be in this order\n\
<author_name> <book_name> <language or no language> \
<status or no status>"
        )
        return 1
    # check for author if found get or else create
    author, created_1 = Author.objects.get_or_create(author=args[0])
    try:
        lang_code = args[2]
    except IndexError:
        book, created_2 = Book.objects.get_or_create(book=args[1], author_name=author)
    else:
        language = Language.objects.get(language=lang_code)
        book, created_3 = Book.objects.get_or_create(
            book=args[1], author_name=author, language_name=language,
        )
    try:
        status_code = args[3]
    except IndexError:
        book_instance = Instance(
            book_name=book,
        )
        book_instance.save()
    else:
        status = Status.objects.get(status=status_code)
        book_instance = Instance(
            book_name=book,
            status_name=status,
        )
        book_instance.save()
    return 0
