
const mysql = require('mysql2');

const connection = mysql.createConnection({
  host: '195.35.45.44', 
  user: 'root',  
  password: 'vikram123',  
  database: 'predict_model'  
});

connection.connect(error => {
  if (error) throw error;
  console.log('Successfully connected to the database.');
});

module.exports = connection;
