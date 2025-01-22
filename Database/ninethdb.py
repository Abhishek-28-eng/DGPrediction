import pandas as pd
import pymysql

# Database connection configuration
db_config = {
    'host': '195.35.45.44',  # Replace with your MySQL host
    'user': 'root',          # Replace with your MySQL username
    'password': 'vikram123', # Replace with your MySQL password
    'database': 'predict_model'  # Replace with your database name
}

def fetch_data_from_mysql():
    """
    Fetch data from the MySQL database and return it as a Pandas DataFrame.
    """
    try:
        # Establish connection to the database
        db_connection = pymysql.connect(**db_config)
        cursor = db_connection.cursor()

        # SQL query to fetch all records from the table
        fetch_query = "SELECT * FROM studnineth_marks"
        cursor.execute(fetch_query)

        # Retrieve data and column names
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Convert to DataFrame
        df = pd.DataFrame(results, columns=column_names)
        return df

    except Exception as e:
        print(f"Error fetching data from MySQL: {e}")
        return None

    finally:
        # Clean up database connections
        if 'cursor' in locals():
            cursor.close()
        if 'db_connection' in locals():
            db_connection.close()

# Fetch data and store it in a global variable
nineth_std = fetch_data_from_mysql()

if nineth_std is not None:
    print("Data fetched successfully and stored in 'nineth_std'.")
else:
    print("Failed to fetch data.")
