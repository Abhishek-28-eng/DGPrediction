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
from Seventh_final_Interest import merged_df7th
from Eight import df_8th

# Ensure 'Interest' columns are strings for processing
merged_df7th["Final_Interests_7th"] = merged_df7th["Final_Interests_7th"].astype(str)
df_8th["Interest"] = df_8th["Interest"].astype(str)

# Merge the existing final_merged_df with the 8th standard dataset
final_merged_with_8th = pd.merge(
    merged_df7th, 
    df_8th[["Unique_ID", "Interest"]], 
    on="Unique_ID", 
    how="inner", 
    suffixes=("", "_8th")  # Added suffix to avoid name conflicts
)

# Check column names after the merge to ensure correct references
#print(final_merged_with_8th.columns)

# Function to handle interests across all standards (5th, 6th, 7th, and 8th)
def handle_interests_8th(row):
    # Adjust column names if suffixes are added during the merge
    interests_7th = set(subject.strip() for subject in row["Final_Interests_7th"].split(","))
    interests_8th = set(subject.strip() for subject in row["Interest_8th"].split(","))
    
    # Find common subjects
    common = interests_7th.intersection(interests_8th)
    
    # If common subjects exist, take those from 7th and all from 8th
    if common:
        result = list(common) + list(interests_8th)
    # If no common subjects, take all unique subjects
    else:
        result = list(interests_7th.union(interests_8th))
    
    # Return as a comma-separated string
    return ", ".join(sorted(set(result)))

# Apply the function to determine final interests across all standards
final_merged_with_8th["Final_Interests_8th"] = final_merged_with_8th.apply(handle_interests_8th, axis=1)

# Save the results to a new CSV file
# output_path = "Final_Interests_5th_6th_7th_8th.csv"
# final_merged_with_8th.to_csv(output_path, index=False)
# print(f"Results saved to {output_path}")

# Display the resulting DataFrame
final_merged_with_8th
print(final_merged_with_8th.columns)