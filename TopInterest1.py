import pandas as pd
import numpy as np
import sys
import json
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier

# Simulated imports for required DataFrame
from GRFI import merged_df
import sys
sys.path.append('./src')
import Tenth_final_Interest
sys.path.append('./src/GrowthRate')
import OverallGr

# Access the dataframe
overall_growth_df = OverallGr.overall_growth_df
final_merged_with_10th = Tenth_final_Interest.final_merged_with_10th

# Function to compute interest based on Computed_Final_Interests and overall growth rates
def compute_interest(row):
    growth_rates = row.filter(like="_Overall_Growth")
    computed_interests = row["Computed_Final_Interests"].split(", ")
    
    # Filter growth rates for subjects in Computed_Final_Interests
    subject_growth = {
        subject: growth_rates.get(subject + "_Overall_Growth", 0)
        for subject in computed_interests
    }
    return subject_growth if subject_growth else {}

# Apply the function to compute interest
merged_df["Interest_Subjects"] = merged_df.apply(compute_interest, axis=1)

# Expand interest subjects into separate columns
interest_df = merged_df["Interest_Subjects"].apply(pd.Series)

# Combine with the original DataFrame
result_df = pd.concat([merged_df, interest_df], axis=1)

# Prepare the output DataFrame
output_df = result_df[["Unique_ID", "Computed_Final_Interests"] + interest_df.columns.tolist()]
output_df = output_df.fillna(0)

# Output the result as JSON
if __name__ == "__main__":
    json_result = output_df.to_json(orient="records")
    print(json_result)

# Specify the file name
file_path = 'data.json'

# Open the file in write mode and save the JSON data
with open(file_path, 'w') as json_file:
    json.dump(json_result, json_file, indent=4)  # Indent for better readability

