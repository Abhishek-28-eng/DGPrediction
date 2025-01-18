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
from Growthrate import df_growthrate

# Define the subjects present in both 9th and 10th standards
# Modify as per your dataset
subjects_9_to_10 = ["Marathi", "Urdu", "Hindi", "English", "History", "Science", 
                    "Geography", "Drawing", "Sports", "Environmental Studies", "Algebra", 
                    "Geometry", "Computer", "Defence", "Sanskrit"]

# Calculate Growth 9th to 10th
year = 9
next_year = 10
growth_9_to_10 = {"Student_id": df_growthrate["Student_id"]}  # Start with Unique_ID

for subject in subjects_9_to_10:
    col_9 = f"{subject}_{year}"
    col_10 = f"{subject}_{next_year}"
    
    if col_9 in df_growthrate.columns and col_10 in df_growthrate.columns:
        # Only calculate growth where both values are not NaN
        condition = df_growthrate[col_9].notna() & df_growthrate[col_10].notna()
        growth_9_to_10[f"{subject}_Growth_{year}_to_{next_year}"] = np.where(
            condition, df_growthrate[col_10] - df_growthrate[col_9], np.nan
        )
    else:
        growth_9_to_10[f"{subject}_Growth_{year}_to_{next_year}"] = np.nan

# Create DataFrame for the growth calculations
growth_9_to_10_df = pd.DataFrame(growth_9_to_10)

growth_9_to_10_df = growth_9_to_10_df.drop(columns=["Sanskrit_Growth_9_to_10"], axis=1)
growth_9_to_10_df

# Debugging: Check the final DataFrame for growth
print("Growth 9th to 10th:")
#print(growth_9_to_10_df.head())
growth_9_to_10_df

# Optionally, save the growth to CSV file
#growth_9_to_10_df.to_csv("Growth_9_to_10.csv", index=False)