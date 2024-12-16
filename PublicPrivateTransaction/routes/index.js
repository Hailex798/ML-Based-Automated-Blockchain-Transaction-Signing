var express = require('express');
var router = express.Router();
var fs = require('fs');
var csvParser = require('csv-parser');
var path = require('path');

console.log("Hello World")

router.get('/', function(req, res, next) {
  res.render('index');
});

router.get('/:page', function(req, res, next) {
  res.render(req.params.page, {page: req.params.page});
});

// Route for /keys which loads transaction data from CSV
router.get('/keys', function (req, res, next) {
  const transactions = [];
  const csvFilePath = path.join(__dirname, '../TransactionDetails/transactions.csv'); // Adjust the path if needed

  console.log(transactions);
  console.log(csvFilePath)

  // Read the CSV file
  fs.createReadStream(csvFilePath)
    .pipe(csvParser())
    .on('data', (row) => transactions.push(row)) // Push each row to transactions
    .on('end', () => {
      // Log the data to ensure it's being read correctly
      console.log(transactions);
      
      // Pass the transactions array to the keys.pug template
      res.render('keys', { transactions });
    })
    .on('error', (err) => {
      console.error('Error reading CSV:', err);
      res.render('keys', { transactions: [], error: 'Error reading transactions.' });
    });
});

module.exports = router;
