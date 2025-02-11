import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from Gr_5th_6th import growth_5_to_6_df
from Gr_6th_7th import growth_6_to_7_df
from Gr_7th_8th import growth_7_to_8_df
from Gr_8th_9th import growth_8_to_9_df
from Gr_9th_10th import growth_9_to_10_df

# Merge all growth DataFrames on Unique_ID
overall_growth_df = growth_5_to_6_df.merge(growth_6_to_7_df, on="Student_id", how="outer") \
                                    .merge(growth_7_to_8_df, on="Student_id", how="outer") \
                                    .merge(growth_8_to_9_df, on="Student_id", how="outer") \
                                    .merge(growth_9_to_10_df, on="Student_id", how="outer")

# Fill NaN values with 0 for all growth columns
overall_growth_df = overall_growth_df.fillna(0)

# Initialize a dictionary to store overall growth rates
overall_growth = {"Student_id": overall_growth_df["Student_id"]}

# List of general subjects across multiple years
general_subjects = ["Marathi", "Urdu", "Hindi", "English", "History", "Science", 
                    "Geography", "Drawing", "Sports", "Environmental Studies", "Math", 
                    "Computer"]

# Calculate the overall growth rate for general subjects
for subject in general_subjects:
    # Collect all growth columns for the subject
    growth_columns = [col for col in overall_growth_df.columns if subject in col and "Growth" in col]
    
    # Calculate the mean growth for the subject across all years
    overall_growth[f"{subject}_Overall_Growth"] = overall_growth_df[growth_columns].mean(axis=1)

# Special handling for Algebra, Geometry, and Defence
special_subjects = ["Algebra", "Geometry", "Defence"]

for subject in special_subjects:
    # Collect growth columns for the subject
    growth_columns = [col for col in overall_growth_df.columns if subject in col and "Growth" in col]
    
    # Calculate overall growth as sum divided by 1 (since they exist in 9th to 10th only)
    overall_growth[f"{subject}_Overall_Growth"] = overall_growth_df[growth_columns].sum(axis=1)

# Convert to DataFrame
overall_growth_df = pd.DataFrame(overall_growth)

# Save the result to a CSV file
overall_growth_df.to_csv("Overall_Growth_5_to_10.csv", index=False)

# Display the result
print("Overall Growth Rates:")
#print(overall_growth_df.head())
overall_growth_df
overall_growth_df.dtypes

