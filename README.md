# Redux notes:
## Last updated 3/1/2020

### Known Bugs:
- Links to Book pages from an Author page aren't working. The routing is set to 'book/<isbn>' but when you're on an Author's page, you're already at 'author/<author_id>', so it just appends that to the relative URL and ends up looking like 'author/121/book/393354377', which breaks.
- Reviews/Ratings displaying twice each on Book pages. Issue with SQL?
- Bug with Genre pages: it will only display single Genre pages for which there are at least one Book. This means you can't delete genres that have no books, which is a problem. Because of that, I haven't been able to test deleting genres yet.

### Still Needs to be Built Out:
- Book covers not implemented
- Author pictures not implemented
- Tiny search not implemented
- Advanced search not implemented
- Displaying or searching by average star rating of books not implemented
- After adding a Book, Genre, Author, etc. the server returns a success message, which is a plain HTML message that takes the user away from the main site. We need to show the user a success message without seeming to depart from the site / take them away from navigation. Multiple possible options for this, including a pop-up, or a success message appended into the DOM.
- On Add Book: need more work to be able to add New Author at the same time. Currently does not read/store information from the modal.
- On Add Book: need additional server logic to check to see if a Book is being added without Author information (e.g. if they intend to add it later)
- On Add Book: need additional validation to see if user is attempting to add a Book that already exists. This screws up the insert so that other Book data may not be inserted correctly alongside the Book entry.
- On See All Books and individual Book pages, only one Author displays, even when there are multiple Authors. On Books, this is because I grouped by ISBN. Just needs to be tweaked, and Jinja code added to the HTML to display multiple authors when present. Logic can be copied from the Author page, where multiple books by same Author are shown.
- On Add Genre: Possibly need additional validation to make sure user is not adding an existing Genre.
- On Add Book: Possibly need additional validation to make sure user is not adding an existing Book.
- On Add Author: Possibly need additional validation to make sure user is not adding an existing Author.

### Other Issues:
- Non-Bootstrap (custom) CSS not being passed to dynamically generated pages, affecting appearance of Navbar and other styled details.
- Is there another way to assign auto-incrementing primary keys to items being inserted into tables other than the way it is currently implemented? I.e., is there a SQL function to do this neatly, rather than calling something like MAX(Genres.genre_id) and then incrementing it by 1 manually before an insert?

### Unknown / Danger:
- The functionality to delete a Genre is partially built, but doesn't check to see if a Genre has Books still associated with it. I have no clue what happens if you try to delete a Genre with Books still in it.
