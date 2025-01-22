import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier

# Add module paths and import the host module
sys.path.append('./Database')
import eightdb

# Load the fifth_std dataframe
data_8th = eightdb.eight_std

data_8th.dtypes

df_8th = data_8th.drop(['Student_Name'], axis=1)
df_8th

# df_8th.insert(0, 'Unique_ID', [f"stud_{i}" for i in range(1, len(df_8th) + 1)])
# df_8th

# df_8th=df_8th.iloc[:10001]
# df_8th

# Ensure all subject columns are numeric
df_8th.iloc[:, 1:] = df_8th.iloc[:, 1:].apply(pd.to_numeric, errors="coerce")

# Function to find top and second-top subjects excluding Unique_ID
def find_top_interests(row):
    # Exclude the Unique_ID column
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

# Apply the function to find the Interest column
df_8th["Interest"] = df_8th.apply(find_top_interests, axis=1)
df_8th
print(f"Dataframe created successfully")
# file_path = "Latest8th.csv"  # Specify your desired file path
# new_8th.to_csv(file_path, index=False)  # Save the DataFrame without the index
# print(f"CSV file saved")
