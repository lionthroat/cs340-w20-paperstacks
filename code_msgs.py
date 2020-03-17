def Messages():
    messages = [
        'No action taken', # Code 0: No action
        'Success! Book has been updated.', # Code 1: Book edit success
        'Book edit fail', # Code 2: Book edit fail
        'Success! The book was added to Paperstacks. Thanks for your contribution!', # Code 3: Book add success
        'Error: Book was not added successfully. This may be because the ISBN-10 is already registered to a book entry on Paperstacks. Please search for books before attempting to add them.', # Code 4: Book add fail
        'Success: The book was deleted from Paperstacks! (But why did you want to? Remember, you can always edit and existing book!)', # Code 5: Book delete success
        'Error: Cannot delete this book, as it will leave one or more authors not associated to a book. Authors must have at least one book on Paperstacks. You may choose to delete the author first.', # Code 6: Book delete fail
        'Author edit success', # Code 7: Author edit success
        'Author edit fail', # Code 8: Author edit fail
        'Author add success', # Code 9: Author add success
        'Author add fail', # Code 10: Author add fail
        'Author delete success', # Code 11: Author delete success
        'Author delete fail', # Code 12: Author delete fail
        'Review edit success', # Code 13: Review edit success
        'Review edit fail', # Code 14: Review edit fail
        'Thank you! Reviews and Ratings make Paperstacks a better site.', # Code 15: Review add success
        'Review add fail', # Code 16: Review add fail
        'Success: The selected review removed.', # Code 17: Review delete success
        'Review delete fail', # Code 18: Review delete fail
        'Success: The selected rating was updated.', # Code 19: Rating edit success
        'Rating edit fail', # Code 20: Rating edit fail
        'Rating add success', # Code 21: Rating add success
        'Rating add fail', # Code 22: Rating add fail
        'Success: The selected rating was removed.', # Code 23: Rating delete success
        'Rating delete fail', # Code 24: Rating delete fail
        'Genre edit success', # Code 25: Genre edit success
        'Genre edit fail', # Code 26: Genre edit fail
        'Genre add success', # Code 27: Genre add success
        'Genre add fail', # Code 28: Genre add fail
        'Genre delete success', # Code 29: Genre delete success
        'Genre delete fail', # Code 30: Genre delete fail
        'The book was added to Paperstacks! However, you did not select an author or did not enter all information required for adding a new author. You may edit the book or add a new author at any time.', # Code 31: Book added but without author(s)
        'Success! You added a new book and new author to Paperstacks! Thanks for your contribution!' # Code 32: Book AND Author added success
    ]
    return messages
