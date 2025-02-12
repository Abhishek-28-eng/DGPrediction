const express = require('express');
const router = express.Router();
const db = require('../db');

// Define the subjects and their corresponding column prefixes
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
    'Environmental Studies': 'Environmental_Studies',
    'Computer': 'Computer',
    'Math': 'Math',  // Special case for Math (splitting after 8th)
    'Defence': 'Defence' // Defence subject added after 8th standard
};

// List of tables representing different growth stages
const tables = [
    'Growth_5_to_6',
    'Growth_6_to_7',
    'Growth_7_to_8',
    'Growth_8_to_9',
    'Growth_9_to_10'
];

// API to fetch all subjects' growth data for a student
router.get('/:id', async (req, res) => {
    const studentId = req.params.id;

    try {
        let results = {};

        // Loop through each subject
        for (const subject in subjectPrefixMap) {
            let subjectGrowth = [];

            // Loop through each growth table
            for (const table of tables) {
                let growthData = {};

                if (subject === 'Math' && (table === 'Growth_8_to_9' || table === 'Growth_9_to_10')) {
                    // After 8th standard, Math splits into Algebra and Geometry
                    const algebraColumn = `Algebra_${table}`;
                    const geometryColumn = `Geometry_${table}`;

                    // Query to get Algebra and Geometry growth data
                    const sqlQuery = `SELECT ${algebraColumn}, ${geometryColumn} FROM ${table} WHERE Student_id = ?`;
                    const [rows] = await db.promise().query(sqlQuery, [studentId]);

                    if (rows.length > 0) {
                        // Calculate the final growth as the average of Algebra and Geometry
                        const algebraGrowth = rows[0][algebraColumn] || 0;
                        const geometryGrowth = rows[0][geometryColumn] || 0;
                        const finalMathGrowth = (algebraGrowth + geometryGrowth) / 2;

                        growthData = {
                            table,
                            growthRate: finalMathGrowth
                        };
                    } else {
                        growthData = { table, growthRate: null };
                    }
                } 
                else if (subject === 'Defence' && (table === 'Growth_8_to_9' || table === 'Growth_9_to_10')) {
                    // Defence subject added only after 8th standard
                    const defenceColumn = `Defence_${table}`;
                    const sqlQuery = `SELECT ${defenceColumn} FROM ${table} WHERE Student_id = ?`;
                    const [rows] = await db.promise().query(sqlQuery, [studentId]);

                    if (rows.length > 0) {
                        growthData = {
                            table,
                            growthRate: rows[0][defenceColumn]
                        };
                    } else {
                        growthData = { table, growthRate: null };
                    }
                } 
                else if (subject !== 'Defence') {
                    // Handle other subjects normally
                    const columnName = `${subjectPrefixMap[subject]}_${table}`;
                    const sqlQuery = `SELECT ${columnName} FROM ${table} WHERE Student_id = ?`;
                    const [rows] = await db.promise().query(sqlQuery, [studentId]);

                    if (rows.length > 0) {
                        growthData = {
                            table,
                            growthRate: rows[0][columnName]
                        };
                    } else {
                        growthData = { table, growthRate: null };
                    }
                }

                subjectGrowth.push(growthData);
            }

            results[subject] = subjectGrowth;
        }

        // Return the structured results
        res.json({ studentId, subjects: results });

    } catch (err) {
        console.error('Error fetching student growth data:', err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

module.exports = router;
