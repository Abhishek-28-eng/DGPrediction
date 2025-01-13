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
from Seventh import df_7th
from Sixth_final_Interest import merged_df

# Ensure 'Interest' columns are strings for processing
merged_df["Final_Interests"] = merged_df["Final_Interests"].astype(str)
df_7th["Interest"] = df_7th["Interest"].astype(str)

# Merge the existing merged_df with the 7th standard dataset
merged_df7th = pd.merge(
    merged_df, 
    df_7th[["Unique_ID", "Interest"]], 
    on="Unique_ID", 
    how="inner", 
    suffixes=("", "_7th")
)

# Verify the column names after merging
print(merged_df.columns)

# Function to handle interests across 5th, 6th, and 7th standards
def handle_interests_7th(row):
    # Split interests into sets
    interests_5th_6th = set(subject.strip() for subject in row["Final_Interests"].split(","))
    interests_7th = set(subject.strip() for subject in row["Interest"].split(","))  # Adjusted column name
    
    # Find common subjects
    common = interests_5th_6th.intersection(interests_7th)
    
    # If common subjects exist, take those from 5th-6th Final_Interests and all from 7th std
    if common:
        result = list(common) + list(interests_7th)
    # If no common subjects, take all unique subjects
    else:
        result = list(interests_5th_6th.union(interests_7th))
    
    # Return as a comma-separated string
    return ", ".join(sorted(set(result)))

# Apply the function to determine final interests across all three standards
merged_df7th["Final_Interests_7th"] = merged_df7th.apply(handle_interests_7th, axis=1)

# Save the results to a new CSV file
# output_path = "Final_Interests_5th_6th_7th.csv"
# final_merged_df.to_csv(output_path, index=False)
# print(f"Results saved to {output_path}")

# Display the resulting DataFrame
merged_df7th