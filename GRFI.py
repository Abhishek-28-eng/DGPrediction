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
import sys
sys.path.append('./src')
import Tenth_final_Interest
sys.path.append('./src/GrowthRate')

# Import the module
import OverallGr

# Access the dataframe
overall_growth_df = OverallGr.overall_growth_df

final_merged_with_10th = Tenth_final_Interest.final_merged_with_10th

# Merge the two dataframes on Unique_ID
merged_df = pd.merge(overall_growth_df, final_merged_with_10th, on="Unique_ID")

# Function to compute final interested subjects
def compute_final_interests(row):
    # Extract growth rates and final interests for the student
    growth_rates = row.filter(like="_Overall_Growth")
    final_interests = row["Final_Interests_10th"].split(", ")
    
    # Filter subjects with positive growth rates and present in final interests
    interested_subjects = [
        subject.split("_Overall_Growth")[0]
        for subject, rate in growth_rates.items()
        if rate > 0 and subject.split("_Overall_Growth")[0] in final_interests
    ]
    return ", ".join(interested_subjects)

# Apply the function to compute the final interested subjects
merged_df["Computed_Final_Interests"] = merged_df.apply(compute_final_interests, axis=1)

# Save or view the result
merged_df[["Unique_ID", "Final_Interests_10th", "Computed_Final_Interests"]].to_csv("computed_final_interests.csv", index=False)

# Display a sample of the result
merged_df[["Unique_ID", "Final_Interests_10th", "Computed_Final_Interests"]].head(10)