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
                INSERT INTO Growth_8_to_9 (Student_id, Marathi_Growth_8_to_9, Urdu_Growth_8_to_9, Hindi_Growth_8_to_9, English_Growth_8_to_9, History_Growth_8_to_9, Science_Growth_8_to_9, Geography_Growth_8_to_9, Drawing_Growth_8_to_9, Sports_Growth_8_to_9, Environmental_Studies_Growth_8_to_9, Algebra_Growth_8_to_9, Geometry_Growth_8_to_9, Computer_Growth_8_to_9, Defence_Growth_8_to_9)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                row['Student_id'],
                row.get('Marathi_Growth_8_to_9', 0),
                row.get('Urdu_Growth_8_to_9', 0),
                row.get('Hindi_Growth_8_to_9', 0),
                row.get('English_Growth_8_to_9', 0),
                row.get('History_Growth_8_to_9', 0),
                row.get('Science_Growth_8_to_9', 0),
                row.get('Geography_Growth_8_to_9', 0),
                row.get('Drawing_Growth_8_to_9', 0),
                row.get('Sports_Growth_8_to_9', 0),
                row.get('Enviromental_Studies_Growth_8_to_9', 0),
                row.get('Algebra_Growth_8_to_9', 0),
                row.get('Geometry_Growth_8_to_9', 0),
                row.get('Computer_Growth_8_to_9', 0),
                row.get('Defence_Growth_8_to_9', 0),
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
    output_df = pd.read_csv('Growth_8_to_9.csv')  # Replace with actual file path or DataFrame
    store_data_in_mysql(output_df)
