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
from Eight_final_Interest import final_merged_with_8th
from Nineth import df_9th

# Ensure 'Interest' columns are strings for processing
final_merged_with_8th["Final_Interests_8th"] = final_merged_with_8th["Final_Interests_8th"].astype(str)
df_9th["Interest"] = df_9th["Interest"].astype(str)

# Merge the existing final_merged_with_8th with the 9th standard dataset
final_merged_with_9th = pd.merge(
    final_merged_with_8th,
    df_9th[["Unique_ID", "Interest"]],
    on="Unique_ID",
    how="inner",
    suffixes=("", "_9th")
)

# Check column names to ensure proper referencing
print(final_merged_with_9th.columns)

# Function to handle interests across all standards up to 9th
def handle_interests_9th(row):
    # Extract interests for 8th and 9th standard
    interests_8th = set(subject.strip() for subject in row["Final_Interests_8th"].split(","))
    interests_9th = set(subject.strip() for subject in row["Interest_9th"].split(","))
    
    # Find common subjects
    common = interests_8th.intersection(interests_9th)
    
    # If common subjects exist, take those from 8th and all from 9th
    if common:
        result = list(common) + list(interests_9th)
    # If no common subjects, take all unique subjects
    else:
        result = list(interests_8th.union(interests_9th))
    
    # Return as a comma-separated string
    return ", ".join(sorted(set(result)))

# Apply the function to determine final interests across all standards
final_merged_with_9th["Final_Interests_9th"] = final_merged_with_9th.apply(handle_interests_9th, axis=1)

# Save the results to a new CSV file
# output_path = "Final_Interests_5th_6th_7th_8th_9th.csv"
# final_merged_with_9th.to_csv(output_path, index=False)
# print(f"Results saved to {output_path}")

# Display the resulting DataFrame
final_merged_with_9th
print(final_merged_with_9th.columns)