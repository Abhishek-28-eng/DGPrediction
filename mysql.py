import pandas as pd
import pymysql

# Database connection configuration
db_config = {
    'host': '195.35.45.44',  # Change to your MySQL host
    'user': 'root',  # Change to your MySQL username
    'password': 'vikram123',  # Change to your MySQL password
    'database': 'predict_model'  # Database name
}

# Function to store data in MySQL
def store_data_in_mysql(df):
    try:
        # Establishing connection to MySQL
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            # SQL query to insert data
            insert_query = """
                INSERT INTO Prediction (Student_id, Computed_Final_Interests, Marathi, Urdu, Hindi, English, History, Science, Geography, Drawing, Sports, Environmental_Studies, Algebra, Geometry, Computer, Defence)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                row['Student_id'],
                row['Computed_Final_Interests'],
                row.get('Marathi', 0),
                row.get('Urdu', 0),
                row.get('Hindi', 0),
                row.get('English', 0),
                row.get('History', 0),
                row.get('Science', 0),
                row.get('Geography', 0),
                row.get('Drawing', 0),
                row.get('Sports', 0),
                row.get('Enviromental_Studies', 0),
                row.get('Algebra', 0),
                row.get('Geometry', 0),
                row.get('Computer', 0),
                row.get('Defence', 0),
            ))

        # Commit the transaction
        db_connection.commit()

        print("Data inserted successfully.")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        # Close the connection
        if 'db_connection' in locals():
            db_connection.close()
        if 'cursor' in locals():
            cursor.close()

# Example usage
if __name__ == "__main__":
    # Assuming output_df is the DataFrame containing all required data
    # Ensure your DataFrame matches the column names in your database table
    output_df = pd.read_csv('filtered_subjects_growth.csv')  # Replace with actual file path or DataFrame
    store_data_in_mysql(output_df)
