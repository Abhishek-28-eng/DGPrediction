import pandas as pd
import seaborn as sns
import numpy as np
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

# Define the subjects present in both 8th and 9th standards
# Subjects present in both 8th and 9th (modify as needed)
subjects_8_to_9 = ["Marathi", "Urdu", "Hindi", "English", "History", "Science", 
                   "Geography", "Drawing", "Sports", "Environmental Studies", "Algebra", "Geometry", "Computer", "Defence"]

# Calculate Growth 8th to 9th
year = 8
next_year = 9
growth_8_to_9 = {"Student_id": df_growthrate["Student_id"]}  # Start with Unique_ID

for subject in subjects_8_to_9:
    col_8 = f"{subject}_{year}"
    col_9 = f"{subject}_{next_year}"
    
    if col_8 in df_growthrate.columns and col_9 in df_growthrate.columns:
        # Only calculate growth where both values are not NaN
        condition = df_growthrate[col_8].notna() & df_growthrate[col_9].notna()
        growth_8_to_9[f"{subject}_Growth_{year}_to_{next_year}"] = np.where(
            condition, df_growthrate[col_9] - df_growthrate[col_8], np.nan
        )
    else:
        growth_8_to_9[f"{subject}_Growth_{year}_to_{next_year}"] = np.nan

# Create DataFrame for the growth calculations
growth_8_to_9_df = pd.DataFrame(growth_8_to_9)

growth_8_to_9_df["Algebra_Growth_8_to_9"] = growth_8_to_9_df["Algebra_Growth_8_to_9"].fillna(0)
growth_8_to_9_df

growth_8_to_9_df["Geometry_Growth_8_to_9"] = growth_8_to_9_df["Geometry_Growth_8_to_9"].fillna(0)
growth_8_to_9_df

growth_8_to_9_df["Defence_Growth_8_to_9"] = growth_8_to_9_df["Defence_Growth_8_to_9"].fillna(0)
growth_8_to_9_df

# Debugging: Check the final DataFrame for growth
print("Growth 8th to 9th:")
growth_8_to_9_df



# Optionally, save the growth to CSV file
#growth_8_to_9_df.to_csv("Growth_8_to_9.csv", index=False)