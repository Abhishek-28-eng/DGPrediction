import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier
from xgboost import XGBClassifier

# Add module paths and import the host module
sys.path.append('./Database')
import fifthdb

# Load the fifth_std dataframe
df = fifthdb.fifth_std

# Display the first few rows of the dataframe
print("Initial DataFrame:")
print(df.head())

# Display column data types
print("\nDataFrame Data Types:")
print(df.dtypes)

# Drop the 'Student_Name' column
df2_5th = df.drop(['Student_Name'], axis=1)
print("\nDataFrame after dropping 'Student_Name':")
print(df2_5th.head())

# Convert all columns (except 'Student_id') to numeric
df2_5th.iloc[:, 1:] = df2_5th.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

# Define a function to find top and second-top subjects
def find_top_interests(row):
    # Exclude 'Student_id' column
    subject_marks = {subject: mark for subject, mark in row.items() if subject != "Student_id"}
    
    # Find the highest and second-highest marks
    unique_marks = sorted(set(subject_marks.values()), reverse=True)
    if len(unique_marks) >= 2:
        top_marks = unique_marks[:2]  # Top two unique marks
    elif len(unique_marks) == 1:
        top_marks = unique_marks  # Only one unique mark
    else:
        top_marks = []  # No marks present
    
    # Collect all subjects with marks in top_marks
    top_subjects = [subject for subject, mark in subject_marks.items() if mark in top_marks]
    return ", ".join(top_subjects)

# Apply the function to find top interests and add it as a new column
df2_5th["Interest"] = df2_5th.apply(find_top_interests, axis=1)

# Display the updated DataFrame
print("\nUpdated DataFrame with 'Interest' column:")
print(df2_5th.head())

# Save the updated DataFrame to a CSV file
# file_path = "Data/Latest5th.csv"  # Specify your desired file path
# df2_5th.to_csv(file_path, index=False)  # Save the DataFrame without the index
# print(f"\nCSV file saved at: {file_path}")
