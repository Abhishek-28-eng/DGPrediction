const express = require('express');
const router = express.Router();
const db = require('../db');

// API to fetch subject growth data for a student, dynamically handling different subject columns
router.get('/:id/:subject', async (req, res) => {
    const studentId = req.params.id;
    const subject = req.params.subject;
    const tables = [
        'Growth_5_to_6',
        'Growth_6_to_7',
        'Growth_7_to_8',
        'Growth_8_to_9',
        'Growth_9_to_10'
    ];

    // Define the prefix for each subject's growth columns
    const subjectPrefixMap = {
        'Marathi': 'Marathi',
        'Urdu': 'Urdu',
        'Hindi': 'Hindi',
        'English': 'English',
        'History': 'History',
        'Science': 'Science',
        'Geography': 'Geography',
        'Drawing': 'Drawing',
        'Sports': 'Sports',
        'Enviroment': 'Enviroment',
        'Computer': 'Computer'
    };

    // Check if the subject is valid
    if (!subjectPrefixMap[subject]) {
        return res.status(400).json({ error: 'Invalid subject' });
    }

    try {
        const results = {};

        // Loop through each growth table
        for (const table of tables) {
            // Construct the column name dynamically based on the subject
            const columnName = `${subjectPrefixMap[subject]}_${table}`;

            // Query to get the subject's data for the student in this table
            const sqlQuery = `SELECT Student_id, ${columnName} FROM ${table} WHERE Student_id = ?`;
            const [rows] = await db.promise().query(sqlQuery, [studentId]);

            // If the student has data for this subject in the table, store it
            if (rows.length > 0) {
                results[table] = rows[0][columnName];
            } else {
                results[table] = null;  // No data found for this table
            }
        }

        // Return the results
        res.json({ studentId, subject, growth: results });

    } catch (err) {
        console.error('Error fetching student growth data:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
