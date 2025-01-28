const express = require('express');
const router = express.Router();
const db = require('../db'); 

router.get('/growth_6_7', (req, res) => {
    const sqlQuery = 'SELECT * FROM Growth_6_to_7';
  
    db.query(sqlQuery, (err, results) => {
      if (err) {
        console.error('Error fetching growth data:', err);
        res.status(500).send('Server error');
      } else {
        res.json(results);
      }
    });
  });
  
  
  router.get('/growth_6/:id', (req, res) => {
    const studentId = req.params.id;
    const sqlQuery = 'SELECT * FROM Growth_6_to_7 WHERE Student_id = ?';
  
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
  