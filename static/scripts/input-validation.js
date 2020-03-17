function validateISBN(input_isbn) {
     // check length to make sure it is exactly 10 characters long
     if (input_isbn.length != 10) {
          input_isbn.setCustomValidity('Please enter a valid, 10-digit ISBN');
     }
     else {
          // convert to a number and check value
          conv_isbn = Number(input_isbn);
          console.log(conv_isbn);
          if (conv_isbn == "NaN" || !conv_isbn.isInteger()) {
               input_isbn.setCustomValidity('Please enter a valid, 10-digit ISBN');
          }
          else {
               input_isbn.setCustomValidity('');
          }
     }
}
