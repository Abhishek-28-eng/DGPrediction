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
import sys

# Add module paths
sys.path.append('./src')
import Tenth_final_Interest
sys.path.append('./src/GrowthRate')

# Import the module
import OverallGr

# Access the dataframes
overall_growth_df = OverallGr.overall_growth_df
final_merged_with_10th = Tenth_final_Interest.final_merged_with_10th

# Merge the two dataframes on "Student_id"
merged_df = pd.merge(overall_growth_df, final_merged_with_10th, on="Student_id")

# Function to compute final interested subjects
def compute_final_interests(row, threshold=0.01):
    """
    Compute final interests based on growth rates and 10th-grade interests.
    If no positive growth rates, consider near-zero or largest negative growth rates.

    Args:
    row (pd.Series): Row of the DataFrame.
    threshold (float): Threshold for considering near-zero growth rates.

    Returns:
    str: Computed final interests as a comma-separated string.
    """
    # Extract growth rates and final interests for the student
    growth_rates = row.filter(like="_Overall_Growth")
    final_interests = row["Final_Interests_10th"].split(", ")
    
    # Filter subjects with positive growth rates and present in final interests
    positive_growth_subjects = [
        subject.split("_Overall_Growth")[0]
        for subject, rate in growth_rates.items()
        if rate > 0 and subject.split("_Overall_Growth")[0] in final_interests
    ]
    
    # If no positive growth rates, consider near-zero growth rates
    if not positive_growth_subjects:
        positive_growth_subjects = [
            subject.split("_Overall_Growth")[0]
            for subject, rate in growth_rates.items()
            if -threshold <= rate <= threshold and subject.split("_Overall_Growth")[0] in final_interests
        ]
    
    # If still no subjects, choose the subject with the largest negative growth rate
    if not positive_growth_subjects:
        negative_growth_subjects = {
            subject.split("_Overall_Growth")[0]: rate
            for subject, rate in growth_rates.items()
            if rate < 0 and subject.split("_Overall_Growth")[0] in final_interests
        }
        if negative_growth_subjects:
            # Find the subject with the least negative growth rate
            largest_negative_subject = max(negative_growth_subjects, key=negative_growth_subjects.get)
            positive_growth_subjects.append(largest_negative_subject)
    
    return ", ".join(positive_growth_subjects)

# Apply the function to compute the final interested subjects
merged_df["Computed_Final_Interests"] = merged_df.apply(compute_final_interests, axis=1)

# Save the result to a CSV file
merged_df[["Student_id", "Final_Interests_10th", "Computed_Final_Interests"]].to_csv("computed_final_interests.csv", index=False)

# Display a sample of the result
print(merged_df[["Student_id", "Final_Interests_10th", "Computed_Final_Interests"]].head(10))
