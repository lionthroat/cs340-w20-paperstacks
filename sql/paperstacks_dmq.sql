-- READ QUERIES --
-- Get all genre names for listing in add book, home page, and genre list page
select genre_name from Genres;


-- Get all author names for listing in add book and author list page
select author_name from Authors;

-- Get all book names for listing in book list and add author page
select book_title from Books;

-- Get average rating for a given book
select star_rating from Ratings where isbn = :ISBN_selected_from_book_page;

-- Get all reviews for a given book
select review_date, review_content from Reviews where isbn = :ISBN_selected_from_book_page;

-- Get all books for a given author

-- Get all authors for a given book

-- Get all books in a given genre

-- Show all info for given author

-- Show all info for given book

-- Get associated rating for a review

-- Get associated review for a rating

-- Get search results from submitted search page

-- Get search results from simple search in navbar

-- ADD QUERIES --

-- Add book/author relationship --

-- Add book/genre relationship --

-- Add rating/review relationship --

-- Book: add review --

-- Book: add rating --

-- Genre: add genre --

-- Author: add author --

-- Book: add book --

-- UPDATE QUERIES --

-- Book: update title --

-- Book: update ISBN --

-- Author: update description --

-- Rating: update star rating --

-- Rating/review unlink --

-- Review: update content --

-- Genre: update genre name --

-- unlink author/book --

-- unlink book/genre --

-- DELETE QUERIES --

-- delete book --

-- delete author --

-- delete genre --

-- delete rating --

-- delete review --