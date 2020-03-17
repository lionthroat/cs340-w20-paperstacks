---------------------------------------------------------
-- DMQ for Paperstacks --
---------------------------------------------------------
-- Sections:
-- 1. Basic READ
-- 2. Basic ADD
-- 3. Basic UPDATE
-- 4. Basic DELETE
-- 5. /books              (READ)
-- 6. /book/<string:isbn> (READ)
-- 7. Navbar search       (FILTER)
-- 8. Advanced search     (FILTER)
---------------------------------------------------------

-- 1. BASIC READ QUERIES --
-- Get all genre names for listing in add book, home page, and genre list page
SELECT genre_name from Genres;

-- Get all author names for listing in add book and author list page
SELECT author_name from Authors;

-- Get all book names for listing in book list and add author page
SELECT book_title from Books;

-- Get average rating for a given book
SELECT star_rating from Ratings where isbn = %ISBN_SELECTed_from_book_page;

-- Get all reviews for a given book
SELECT review_date, review_content from Reviews where isbn = %ISBN_SELECTed_from_book_page;

-- Get all books for a given author
SELECT book.book_title from Books book
inner join Books_Authors ba on ba.isbn = book.isbn
inner join Authors auth on ba.author_id = auth.author_id
where auth.author_id = %input_author_id;

-- Get all authors for a given book
SELECT author.author_name from Authors auth
inner join Books_Authors ba on ba.author_id = auth.author_id
inner join Books book on ba.isbn = book.isbn
where book.isbn = %input_isbn;

-- Get all books in a given genre
SELECT book.book_title from Books book
inner join Books_Genres bg on bg.isbn = book.isbn
inner join Genres g on bg.genre_id = g.genre_id
where g.genre_id = %input_genre_id;

-- Show all info for given author
SELECT auth.author_name, auth.author_description from Authors auth
where auth.author_id = %input_author_id;

-- Show static info for given book
SELECT book.book_title, book.year_published, book.book_description from Books book where book.isbn = %input_isbn;

-- Get ratings for a given book --
SELECT rating.rating_id from Ratings rating where rating.isbn = %input_isbn;

-- Get associated rating for a review
SELECT rating.star_rating from Ratings rating where rating.review_id = %input_review_id;

-- Get associated review for a rating
SELECT review.review_content from Reviews review where review.rating_id = %input_rating_id;

-- Get search results from submitted search page

-- Get search results from simple search in navbar
SELECT * from Genres where genre_name.contains(%input_string);
SELECT * from Authors where author_name.contains(%input_string);
SELECT * from Books where book_title.contains(%input_string);

-- 2. BASIC ADD QUERIES --

-- Add book/author relationship --
insert into Books_Authors (isbn, author_id) values (%input_isbn, %input_author_id);

-- Add book/genre relationship --
insert into Genres_Books(isbn, genre_id) values (%input_isbn, %input_genre_id);

-- Add rating/review relationship --
update Ratings set review_id= %review_id_input where rating_id = %input_rating_id;
update Reviews set rating_id= %rating_id_input where review_id = %input_review_id;

-- Book: add review --
update Reviews set isbn= %input_isbn where review_id = %input_review_id;

-- Book: add rating --
update Ratings set isbn= %input_isbn where rating_id = %input_rating_id;

-- Genre: add genre --
insert into Genres (genre_name) values (%input_genre_name);;

-- Author: add author --
insert into Authors (author_name, author_description) values (%input_author_name, %input_author_description);

-- Book: add book --
insert into Books (isbn, book_title, year_published, book_description)
values (%input_isbn, %input_book_title, %input_year_published, %input_book_description);

-- 3. BASIC UPDATE QUERIES --

-- Book: update title --
update Books set book_title= %input_book_title where isbn= %input_isbn;

-- Book: update ISBN --
update Books set isbn= %new_isbn where isbn= %old_isbn;

-- Author: update description --
update Authors set author_description= %input_author_description where author_id= %input_author_id;

-- Rating: update star rating --
update Ratings set star_rating= %input_rating where rating_id=%input_id;

-- Rating/review unlink --
update Ratings set review_id=NULL where rating_id=%input_rating;
update Reviews set rating_id=NULL where review_id=%input_review;

-- Review: update content --
update Reviews set review_content=%new_review_content where review_id=%input_id;

-- Genre: update genre name --
update Genres set genre_name=%new_name where genre_id=%input_id;

-- unlink author/book --
delete Books_Authors where isbn=%input_isbn and author_id=%input_author_id;

-- unlink book/genre --
delete Genres_Books where isbn=%input_isbn and genre_id=%input_genre_id;

-- 4. BASIC DELETE QUERIES --

-- delete book --
delete Genres_Books where isbn=%input_isbn;
delete Reviews where isbn=%input_isbn;
delete Ratings where isbn=%input_isbn;
delete Books where isbn=%input_isbn;
delete Authors_Books where isbn=%input_isbn;

-- delete author --
delete Authors_Books where author_id=%input_id;
delete Author where author_id=%input_auth_id;

-- delete genre --
delete Genres where genre_id=%input_id;
delete Genres_Books where genre_id=%input_id;

-- delete rating --
update Reviews set rating_id=NULL where rating_id=%input_id;
delete Ratings where rating_id=%input_id;

-- delete review --
update Ratings set review_id=NULL where review_id=%input_id;
delete Reviews where review_id=%input_id;

---------------------------------------------------------
-- 5. /books READ
-- first query gets all books without known authors
-- second query gets all books with known authors
---------------------------------------------------------
SELECT Books.isbn, Books.book_title from Books WHERE NOT EXISTS(SELECT isbn FROM Books_Authors WHERE Books_Authors.isbn=Books.isbn)

SELECT book.isbn, book.book_title, auth.author_name from Books book JOIN Books_Authors ba on ba.isbn = book.isbn join Authors auth ON auth.author_id = ba.author_id order by book.book_title ASC
---------------------------------------------------------

---------------------------------------------------------
-- 6. /book/<string:isbn> READ
-- first query returns one entry PER genre associated with the book.
-- second query gets all known authors (or none) associated with the book
-- third query calculates the average star rating for the book (if possible)
-- fourth query gets all reviews WITH Ratings
-- fifth query gets all ratings that have no associated Review
---------------------------------------------------------
SELECT book.isbn, book.book_title, book.year_published, book.book_description, genre.genre_name from Books book join Genres_Books gb on gb.isbn = book.isbn join Genres genre on genre.genre_id = gb.genre_id where book.isbn = %isbn

SELECT auth.author_name, auth.author_id from Authors auth JOIN Books_Authors ba ON ba.author_id = auth.author_id where ba.isbn = %isbn

SELECT AVG(star_rating) AS `average_rating`, COUNT(rate.rating_id) AS `rating_count` FROM Ratings rate WHERE rate.isbn = %isbn

SELECT book.isbn, rate.rating_id, rate.review_id, rate.star_rating, rate.rating_date, rev.review_content from Books book join Ratings rate on rate.isbn = book.isbn join Reviews rev on rev.isbn = rate.isbn where book.isbn = %isbn AND rev.rating_id = rate.rating_id AND rate.review_id = rev.review_id

SELECT * FROM Ratings WHERE isbn = %isbn AND review_id IS NULL
---------------------------------------------------------

---------------------------------------------------------
-- 7. Navbar search (FILTER)
-- This performs simple substring searches of Books, Authors, and Genres
---------------------------------------------------------
SELECT book.isbn, book.book_title FROM Books book WHERE book.book_title LIKE '%query%'
SELECT auth.author_id, auth.author_name FROM Authors auth WHERE auth.author_name LIKE '%query%'
SELECT genre.genre_id, genre.genre_name FROM Genres genre WHERE genre.genre_name LIKE '%query%'
---------------------------------------------------------

---------------------------------------------------------
-- 8. Advanced search (FILTER)
-- This performs advanced searches of Books by many optional criteria.
-- Note: this is ONE sample query, for more complete list of how optional
-- criteria affect the actual query run, please see code in run.py
---------------------------------------------------------
SELECT book.isbn, book.book_title, COUNT(rev.review_id) AS `num_reviews`, ROUND(AVG(rate.star_rating)) AS `average_rating`, auth.author_id, auth.author_name FROM Books book JOIN Books_Authors ba ON ba.isbn = book.isbn JOIN Authors auth ON auth.author_id = ba.author_id JOIN Genres_Books gb on gb.isbn = book.isbn JOIN Genres genre ON genre.genre_id = gb.genre_id JOIN Ratings rate ON rate.isbn = book.isbn JOIN Reviews rev ON rev.isbn = book.isbn GROUP BY book.isbn HAVING num_reviews > 0 AND average_rating = %rating ORDER BY book.book_title ASC
---------------------------------------------------------
