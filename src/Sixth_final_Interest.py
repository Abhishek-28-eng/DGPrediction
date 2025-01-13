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
from Fifth import df2_5th
from Sixth import df2_6th

# Ensure the datasets have a unique identifier column (e.g., "Unique_ID")
if "Unique_ID" not in df2_5th.columns or "Unique_ID" not in df2_6th.columns:
    raise ValueError("Both datasets must contain a 'Unique_ID' column.")

# Merge the datasets on the Unique_ID column
merged_df = pd.merge(df2_5th[["Unique_ID", "Interest"]], df2_6th[["Unique_ID", "Interest"]], on="Unique_ID", suffixes=("_5th", "_6th"))

# Function to handle interests based on conditions
def handle_interests(row):
    # Split interests into sets
    interests_5th = set(subject.strip() for subject in row["Interest_5th"].split(","))
    interests_6th = set(subject.strip() for subject in row["Interest_6th"].split(","))
    
    # Find common subjects
    common = interests_5th.intersection(interests_6th)
    
    # If common subjects exist, take those from 5th std and all from 6th std
    if common:
        result = list(common) + list(interests_6th)
    # If no common subjects, take all unique subjects
    else:
        result = list(interests_5th.union(interests_6th))
    
    # Return as a comma-separated string
    return ", ".join(sorted(set(result)))

# Apply the function to determine final interests
merged_df["Final_Interests"] = merged_df.apply(handle_interests, axis=1)
merged_df
