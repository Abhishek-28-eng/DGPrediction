import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
from GRFI import merged_df
import sys
sys.path.append('./src')
import Tenth_final_Interest
sys.path.append('./src/GrowthRate')

# Import the module
import OverallGr

# Access the dataframe
overall_growth_df = OverallGr.overall_growth_df

final_merged_with_10th = Tenth_final_Interest.final_merged_with_10th

# Function to compute interest based on Computed_Final_Interests and overall growth rates
def compute_interest(row):
    # Extract growth rates for subjects in Computed_Final_Interests
    growth_rates = row.filter(like="_Overall_Growth")
    computed_interests = row["Computed_Final_Interests"].split(", ")
    
    # Filter growth rates for subjects in Computed_Final_Interests
    subject_growth = {
        subject: growth_rates[subject + "_Overall_Growth"]
        for subject in computed_interests
        if subject + "_Overall_Growth" in growth_rates
    }
    
    # Check for positive growth rates
    positive_growth = {k: v for k, v in subject_growth.items() if v > 0}
    if positive_growth:
        # Return subjects with positive growth rates
        return positive_growth
    
    # If no positive growth, find the subject with the largest negative growth rate (closest to zero)
    negative_growth = {k: v for k, v in subject_growth.items() if v < 0}
    if negative_growth:
        # Find the subject with the maximum (least negative) growth rate
        largest_negative_subject = max(negative_growth, key=negative_growth.get)
        return {largest_negative_subject: negative_growth[largest_negative_subject]}
    
    # If no valid growth rates, return an empty dictionary
    return {}

# Apply the function to compute interest
merged_df["Interest_Subjects"] = merged_df.apply(compute_interest, axis=1)

# Expand the interest subjects into separate columns
interest_df = merged_df["Interest_Subjects"].apply(pd.Series)

# Combine with the original DataFrame
result_df = pd.concat([merged_df, interest_df], axis=1)

# Save or view the result
output_df = result_df[["Student_id", "Computed_Final_Interests"] + interest_df.columns.tolist()]

# Fill null values with 0 (if needed)
output_df = output_df.fillna(0)

# Save the result to a CSV file
output_df.to_csv("filtered_subjects_growth.csv", index=False)

# Display a sample of the result
print(output_df)
