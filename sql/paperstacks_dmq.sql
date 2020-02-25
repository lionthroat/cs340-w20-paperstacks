-- READ QUERIES --
-- Get all genre names for listing in add book, home page, and genre list page
select genre_name from Genres;

-- Get all author names for listing in add book and author list page
select author_name from Authors;

-- Get all book names for listing in book list and add author page
select book_title from Books;

-- Get average rating for a given book
select star_rating from Ratings where isbn = %ISBN_selected_from_book_page;

-- Get all reviews for a given book
select review_date, review_content from Reviews where isbn = %ISBN_selected_from_book_page;

-- Get all books for a given author
select book.book_title from Books book
inner join Books_Authors ba on ba.isbn = book.isbn
inner join Authors auth on ba.author_id = auth.author_id
where auth.author_id = %input_author_id;

-- Get all authors for a given book
select author.author_name from Authors auth 
inner join Books_Authors ba on ba.author_id = auth.author_id
inner join Books book on ba.isbn = book.isbn 
where book.isbn = %input_isbn;

-- Get all books in a given genre
select book.book_title from Books book
inner join Books_Genres bg on bg.isbn = book.isbn 
inner join Genres g on bg.genre_id = g.genre_id 
where g.genre_id = %input_genre_id;

-- Show all info for given author
select auth.author_name, auth.author_description from Authors auth
where auth.author_id = %input_author_id;

-- Show static info for given book
select book.book_title, book.year_published, book.book_description from Books book where book.isbn = %input_isbn;

-- Get ratings for a given book --
select rating.rating_id from Ratings rating where rating.isbn = %input_isbn;

-- Get associated rating for a review
select rating.star_rating from Ratings rating where rating.review_id = %input_review_id;

-- Get associated review for a rating
select review.review_content from Reviews review where review.rating_id = %input_rating_id;

-- Get search results from submitted search page

-- Get search results from simple search in navbar
select * from Genres where genre_name.contains(%input_string);
select * from Authors where author_name.contains(%input_string);
select * from Books where book_title.contains(%input_string);

-- ADD QUERIES --

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

-- UPDATE QUERIES --

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

-- DELETE QUERIES --

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