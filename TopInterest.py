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
# Function to compute percentage of interest for each subject
def compute_interest_percentage(row):
    # Extract growth rates for subjects in Computed_Final_Interests
    growth_rates = row.filter(like="_Overall_Growth")
    computed_interests = row["Computed_Final_Interests"].split(", ")
    
    # Filter growth rates for subjects in Computed_Final_Interests
    subject_growth = {
        subject: growth_rates[subject + "_Overall_Growth"]
        for subject in computed_interests
        if subject + "_Overall_Growth" in growth_rates
    }
    
    # If no subjects have positive growth, return empty dict
    if not subject_growth:
        return {}
    
    # Normalize growth rates to percentages
    max_growth = max(subject_growth.values())
    percentage_interests = {subject: (rate / max_growth) * 100 for subject, rate in subject_growth.items()}
    return percentage_interests

# Apply the function to compute interest percentages
merged_df["Interest_Percentages"] = merged_df.apply(compute_interest_percentage, axis=1)

# Expand percentages into separate columns for better readability
percentages_df = merged_df["Interest_Percentages"].apply(pd.Series)

# Combine with the original DataFrame
result_df = pd.concat([merged_df, percentages_df], axis=1)


# Save or view the result
output_df = result_df[["Unique_ID", "Computed_Final_Interests", "Interest_Percentages"] + percentages_df.columns.tolist()] #.to_csv("interest_percentages2.csv", index=False)
output_df

# Display a sample of the result
# result_df[["Unique_ID", "Computed_Final_Interests", "Interest_Percentages"]]


