import pymysql

# Database connection configuration
db_config = {
    'host': '195.35.45.44',  # Change to your MySQL host
    'user': 'root',          # Change to your MySQL username
    'password': 'vikram123', # Change to your MySQL password
    'database': 'MGVP'  # Database name
}
print("hii")

# Table names for unit tests
unit_test_tables = [
    "unittest_7th_1",
    "unittest_7th_2",
    "unittest_7th_3",
    "unittest_7th_4",
    "unittest_mid_7th",
    "unittest_final_7th"
]

# Subject names
subjects = [
    "Marathi", "Urdu", "Hindi", "English", "History", "Science", 
    "Geography", "Drawing", "Sports", "Environmental_Studies", "Math", "Computer"
]

# Maximum marks for all unit tests combined (out of 240)
max_total_marks = 240

try:
    # Connect to the database
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor()

    # Create a new table to store the percentages if it doesn't already exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS unittest_7th_average (
            Student_id INT PRIMARY KEY,
            Marathi INT, Urdu INT, Hindi INT, English INT, History INT,
            Science INT, Geography INT, Drawing INT, Sports INT,
            Environmental_Studies INT, Math INT, Computer INT,
            final_mark FLOAT  
        )
    """)

    # Get distinct student IDs
    cursor.execute(f"""
        SELECT DISTINCT Student_id 
        FROM {unit_test_tables[0]}
    """)
    students = [row[0] for row in cursor.fetchall()]

    for Student_id in students:
        subject_totals = {subject: 0 for subject in subjects}

        # Sum marks for each subject across all unit test tables
        for table in unit_test_tables:
            query = f"""
                SELECT 
                    {', '.join([f"COALESCE({subject}, 0)" for subject in subjects])}
                FROM {table} 
                WHERE Student_id = %s
            """
            cursor.execute(query, (Student_id,))
            row = cursor.fetchone()
            if row:
                for i, subject in enumerate(subjects):
                    subject_totals[subject] += row[i]

        # Convert total marks to percentages (out of 100) and round to integer
        subject_percentages = {subject: int((total / max_total_marks) * 100) for subject, total in subject_totals.items()}

        # Calculate total percentage across all subjects
        total_percentage = sum(subject_percentages.values()) / len(subject_percentages)

        # Insert or update percentages and final_mark into the new table
        insert_query = f"""
            INSERT INTO unittest_7th_average (
                Student_id, {', '.join(subjects)}, final_mark
            ) VALUES (
                %s, {', '.join(['%s' for _ in subjects])}, %s
            ) ON DUPLICATE KEY UPDATE 
            {', '.join([f"{subject} = VALUES({subject})" for subject in subjects])}, 
            final_mark = VALUES(final_mark)
        """
        cursor.execute(insert_query, (Student_id, *subject_percentages.values(), int(total_percentage)))

    # Commit changes
    connection.commit()
    print("Subject percentages and total percentage (final_mark) calculated and stored successfully.")

except pymysql.Error as e:
    print(f"Database Error: {e}")

finally:
    if connection:
        connection.close()
