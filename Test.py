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
        # Establish connection
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # SQL query to insert data
        insert_query = """
            INSERT INTO Overall_GR (Student_id, Marathi_Overall_Growth, Urdu_Overall_Growth, Hindi_Overall_Growth, 
                                    English_Overall_Growth, History_Overall_Growth, Science_Overall_Growth, 
                                    Geography_Overall_Growth, Drawing_Overall_Growth, Sports_Overall_Growth, 
                                    Environmental_Studies_Overall_Growth, Algebra_Overall_Growth, 
                                    Geometry_Overall_Growth, Computer_Overall_Growth, Defence_Overall_Growth)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            cursor.execute(insert_query, (
                row['Student_id'],
                row['Marathi_Overall_Growth'] if 'Marathi_Overall_Growth' in df.columns else 0,
                row['Urdu_Overall_Growth'] if 'Urdu_Overall_Growth' in df.columns else 0,
                row['Hindi_Overall_Growth'] if 'Hindi_Overall_Growth' in df.columns else 0,
                row['English_Overall_Growth'] if 'English_Overall_Growth' in df.columns else 0,
                row['History_Overall_Growth'] if 'History_Overall_Growth' in df.columns else 0,
                row['Science_Overall_Growth'] if 'Science_Overall_Growth' in df.columns else 0,
                row['Geography_Overall_Growth'] if 'Geography_Overall_Growth' in df.columns else 0,
                row['Drawing_Overall_Growth'] if 'Drawing_Overall_Growth' in df.columns else 0,
                row['Sports_Overall_Growth'] if 'Sports_Overall_Growth' in df.columns else 0,
                row['Environmental_Studies_Overall_Growth'] if 'Environmental_Studies_Overall_Growth' in df.columns else 0,  # Fixed column name
                row['Algebra_Overall_Growth'] if 'Algebra_Overall_Growth' in df.columns else 0,
                row['Geometry_Overall_Growth'] if 'Geometry_Overall_Growth' in df.columns else 0,
                row['Computer_Overall_Growth'] if 'Computer_Overall_Growth' in df.columns else 0,
                row['Defence_Overall_Growth'] if 'Defence_Overall_Growth' in df.columns else 0
            ))

        # Commit the transaction
        db_connection.commit()
        print("Data inserted successfully.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close cursor first, then connection
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# Example usage
if __name__ == "__main__":
    # Read CSV file into DataFrame
    output_df = pd.read_csv('Overall_Growth_5_to_10.csv')  # Replace with actual file path
    store_data_in_mysql(output_df)
