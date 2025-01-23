const express = require('express');
const router = express.Router();
const db = require('../db'); 

router.get('/growth_9_10', (req, res) => {
    const sqlQuery = 'SELECT * FROM Growth_9_to_10';
  
    db.query(sqlQuery, (err, results) => {
      if (err) {
        console.error('Error fetching growth data:', err);
        res.status(500).send('Server error');
      } else {
        res.json(results);
      }
    });
  });
  
  
  router.get('/growth_9_10/:id', (req, res) => {
    const studentId = req.params.id;
    const sqlQuery = 'SELECT * FROM Growth_9_to_10 WHERE Student_id = ?';
  
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
  