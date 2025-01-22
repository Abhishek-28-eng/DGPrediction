const express = require('express');
const router = express.Router();
const db = require('../db'); 

//Getting all data
router.get('/predictions', (req, res) => {
  const sqlQuery = 'SELECT * FROM Prediction';

  db.query(sqlQuery, (err, results) => {
    if (err) {
      console.error('Error fetching predictions:', err);
      res.status(500).send('Server error');
    } else {
      res.json(results); 
    }
  });
});

// student by Student_id
router.get('/students/:id', (req, res) => {
  const studentId = req.params.id;
  const sqlQuery = 'SELECT * FROM Prediction WHERE Student_id = ?';

  db.query(sqlQuery, [studentId], (err, results) => {
    if (err) {
      console.error('Error fetching student by ID:', err);
      res.status(500).send('Server error');
    } else if (results.length === 0) {
      res.status(404).send('Student not found');
    } else {
      res.json(results[0]); 
    }
  });
});


module.exports = router;
