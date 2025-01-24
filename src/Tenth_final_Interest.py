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
from Nineth_final_Interest import final_merged_with_9th
from Tenth import df_10th

# Final_Interests_7th + Interest_8th = Final_Interests_8th
# Ensure 'Interest' columns are strings for processing
final_merged_with_9th["Final_Interests_9th"] = final_merged_with_9th["Final_Interests_9th"].astype(str)
df_10th["Interest"] = df_10th["Interest"].astype(str)

# Merge the existing final_merged_df with the 8th standard dataset
final_merged_with_10th = pd.merge(
   final_merged_with_9th, 
    df_10th[["Student_id", "Interest"]], 
    on="Student_id", 
    how="inner", 
    suffixes=("", "_10th")  # Added suffix to avoid name conflicts
)

# Check column names after the merge to ensure correct references

# print(final_merged_with_9th.columns)

# Function to handle interests across all standards (5th, 6th, 7th, and 8th)
def handle_interests_10th(row):
    # Adjust column names if suffixes are added during the merge
    interests_9th = set(subject.strip() for subject in row["Final_Interests_9th"].split(","))
    interests_10th = set(subject.strip() for subject in row["Interest_10th"].split(","))
    
    # Find common subjects
    common = interests_9th.intersection(interests_10th)
    
    # If common subjects exist, take those from 7th and all from 8th
    if common:
        result = list(common) + list(interests_10th)
    # If no common subjects, take all unique subjects
    else:
        result = list(interests_9th.union(interests_10th))
    
    # Return as a comma-separated string
    return ", ".join(sorted(set(result)))

# Apply the function to determine final interests across all standards
final_merged_with_10th["Final_Interests_10th"] = final_merged_with_10th.apply(handle_interests_10th, axis=1)

# Save the results to a new CSV file
#output_path = "Final_Interests_5th_6th_7th_8th_9th_10th.csv"
# final_merged_with_10th.to_csv(output_path, index=False)
# print(f"Results saved to {output_path}")

print(final_merged_with_10th.columns)

# Display the resulting DataFrame
final_merged_with_10th
print(final_merged_with_10th)