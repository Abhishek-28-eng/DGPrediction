const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Path to your JSON file
const filePath = path.join(__dirname, 'data.json');

// Middleware to parse JSON requests
app.use(express.json());

// Endpoint to get all data
app.get('/api/students', (req, res) => {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      res.status(500).json({ message: 'Error reading the JSON file', error: err });
      return;
    }
    try {
      const jsonData = JSON.parse(data);
      res.status(200).json(jsonData);
    } catch (parseError) {
      res.status(500).json({ message: 'Error parsing the JSON data', error: parseError });
    }
  });
});

// Endpoint to get data by Unique_ID
app.get('/api/students/:id', (req, res) => {
    const uniqueID = req.params.id;
    fs.readFile(filePath, 'utf8', (err, data) => {
  if (err) {
    return res.status(500).json({ message: 'Error reading the JSON file', error: err.message });
  }
  try {
    const jsonData = JSON.parse(data);
    if (Array.isArray(jsonData) && jsonData.length > 0) {
      const student = jsonData.find(s => s.Unique_ID === uniqueID);
      if (student) {
        res.status(200).json(student);
      } else {
        res.status(404).json({ message: 'Student not found' });
      }
    } else {
      res.status(404).json({ message: 'No students found in the data' });
    }
  } catch (parseError) {
    res.status(500).json({ message: 'Error parsing the JSON data', error: parseError.message });
  }
});
});
  
// Start the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
