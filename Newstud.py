import pandas as pd
import sys
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Add module paths and import the host module
sys.path.append('./Database')
import fifthdb
import sixthdb
import seventhdb
import eightdb
import ninethdb
import tenthdb

# Load the fifth_std dataframe
fifth_std = fifthdb.fifth_std
sixth_std = sixthdb.sixth_std
seventh_std = seventhdb.seventh_std
eight_std = eightdb.eight_std
nineth_std = ninethdb.nineth_std
tenth_std = tenthdb.tenth_std

print(fifth_std.columns)
print(tenth_std.columns)




# Define a function to preprocess data
def preprocess_data(data):
    # One-hot encode subjects
    subjects = pd.get_dummies(data['subject'])
    data = pd.concat([data, subjects], axis=1)
    data.drop('subject', axis=1, inplace=True)
    
    return data

# Define a function to generate a new student ID
def generate_new_student_id(last_id):
    # Extract the numeric part of the ID
    numeric_part = int(last_id[1:])
    
    # Increment the numeric part by 1
    new_numeric_part = numeric_part + 1
    
    # Convert the new numeric part back to a string and pad with zeros
    new_id = 'S' + str(new_numeric_part).zfill(7)
    
    return new_id

# Define a function to fill current year marks
def fill_current_year_marks(data):
    # Define features (X) and target variable (y)
    X = data.drop(['Student_id', 'Student_Name', 'current_year_marks'], axis=1)
    y = data['current_year_marks']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on testing data
    y_pred = model.predict(X_test)
    
    # Evaluate model performance
    mae = mean_absolute_error(y_test, y_pred)
    print(f'MAE for current year marks: {mae:.2f}')
    
    return model

# Define a function to fill previous years' marks
def fill_previous_years_marks(data, filled_current_year_marks):
    # Define features (X) and target variable (y)
    X = data.drop(['Student_id', 'Student_Name', 'previous_years_marks'], axis=1)
    y = data['previous_years_marks']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a Random Forest Regressor model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Make predictions on testing data
    y_pred = model.predict(X_test)
    
    # Evaluate model performance
    mae = mean_absolute_error(y_test, y_pred)
    print(f'MAE for previous years marks: {mae:.2f}')
    
    # Use the trained model to fill previous years' marks for new students
    new_student_data = pd.DataFrame({'current_year_marks': filled_current_year_marks})
    filled_previous_years_marks = model.predict(new_student_data)
    return filled_previous_years_marks

# Preprocess data
all_data = pd.concat([fifth_std, sixth_std, seventh_std, eight_std, nineth_std, tenth_std])

# One-hot encode subjects for 9th and 10th standards
nineth_std = pd.get_dummies(nineth_std, columns=['subject'])
tenth_std = pd.get_dummies(tenth_std, columns=['subject'])

# Recombine the data
all_data = pd.concat([fifth_std, sixth_std, seventh_std, eight_std, nineth_std, tenth_std])

# Preprocess the combined data
all_data = preprocess_data(all_data)

# Fill current year marks and previous years' marks
filled_current_year_marks_model = fill_current_year_marks(all_data)
filled_current_year_marks = filled_current_year_marks_model.predict(all_data.drop(['Student_id', 'Student_Name', 'current_year_marks'], axis=1))

filled_previous_years_marks_model = fill_previous_years_marks(all_data, filled_current_year_marks)
filled_previous_years_marks = filled_previous_years_marks_model.predict(all_data.drop(['Student_id', 'Student_Name', 'previous_years_marks'], axis=1))

# Add the predicted marks to the current datasets
all_data['predicted_current_year_marks'] = filled_current_year_marks
all_data['predicted_previous_years_marks'] = filled_previous_years_marks

# Split the data back into separate DataFrames for each standard
fifth_std = all_data[all_data['standard'] == '5th'].copy()
sixth_std = all_data[all_data['standard'] == '6th'].copy()
seventh_std = all_data[all_data['standard'] == '7th'].copy()
eight_std = all_data[all_data['standard'] == '8th'].copy()
nineth_std = all_data[all_data['standard'] == '9th'].copy()
tenth_std = all_data[all_data['standard'] == '10th'].copy()