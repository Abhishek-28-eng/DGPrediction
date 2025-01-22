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
                INSERT INTO Growth_9_to_10 (Student_id, Marathi_Growth_9_to_10, Urdu_Growth_9_to_10, Hindi_Growth_9_to_10, English_Growth_9_to_10, History_Growth_9_to_10, Science_Growth_9_to_10, Geography_Growth_9_to_10, Drawing_Growth_9_to_10, Sports_Growth_9_to_10, Environmental_Studies_Growth_9_to_10, Algebra_Growth_9_to_10, Geometry_Growth_9_to_10, Computer_Growth_9_to_10, Defence_Growth_9_to_10)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                row['Student_id'],
                row.get('Marathi_Growth_9_to_10', 0),
                row.get('Urdu_Growth_9_to_10', 0),
                row.get('Hindi_Growth_9_to_10', 0),
                row.get('English_Growth_9_to_10', 0),
                row.get('History_Growth_9_to_10', 0),
                row.get('Science_Growth_9_to_10', 0),
                row.get('Geography_Growth_9_to_10', 0),
                row.get('Drawing_Growth_9_to_10', 0),
                row.get('Sports_Growth_9_to_10', 0),
                row.get('Enviromental_Studies_Growth_9_to_10', 0),
                row.get('Algebra_Growth_9_to_10', 0),
                row.get('Geometry_Growth_9_to_10', 0),
                row.get('Computer_Growth_9_to_10', 0),
                row.get('Defence_Growth_9_to_10', 0),
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
    output_df = pd.read_csv('Growth_9_to_10.csv')  # Replace with actual file path or DataFrame
    store_data_in_mysql(output_df)
