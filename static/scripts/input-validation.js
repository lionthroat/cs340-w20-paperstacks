function validateISBN(input_isbn) {
     // check length to make sure it is exactly 10 characters long
     if (input_isbn.value.length != 10) {
          input_isbn.setCustomValidity('Please enter a valid, 10-digit ISBN');
          console.log(input_isbn.value);
     }
     else {
          // convert to a number and check value
          let first_half = input_isbn.value.slice(0, 5);
          let second_half = input_isbn.value.slice(5);
          let conv_isbn_1 = Number(first_half);
          let conv_isbn_2 = Number(second_half);
          if (conv_isbn_1 == "NaN" || !Number.isInteger(conv_isbn_1) || conv_isbn_2 == "NaN" || !Number.isInteger(conv_isbn_2)) {
               input_isbn.setCustomValidity('Please enter a valid, 10-digit ISBN');
               console.log("Not a number");
          }
          else {
               input_isbn.setCustomValidity('');
          }
     }
}
function validateYear(input_year) {
     year = Number(input_year.value);
     console.log(input_year.value)
     if (year == "NaN" || !Number.isInteger(year) || year < 0 || year > 2025) {
          input_year.setCustomValidity('Please enter a valid year');
     }
     else {
          input_year.setCustomValidity('');
     }
}