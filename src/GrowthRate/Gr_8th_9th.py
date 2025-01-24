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
# Define the subjects present in both 8th and 9th standards
subjects_8_to_9 = ["Marathi", "Urdu", "Hindi", "English", "History", "Science", 
                   "Geography", "Drawing", "Sports", "Environmental Studies", "Algebra", "Geometry", "Computer", "Defence"]

# Load the growth data (assuming it's in a DataFrame named df_growthrate)
# Assuming df_growthrate has the columns: ["Student_id", "Marathi_8", "Marathi_9", ... "Defence_9", ...]

# Calculate Growth 8th to 9th
year = 8
next_year = 9
growth_8_to_9 = {"Student_id": df_growthrate["Student_id"]}  # Start with Unique_ID

for subject in subjects_8_to_9:
    col_8 = f"{subject}_{year}"
    col_9 = f"{subject}_{next_year}"
    
    if col_8 in df_growthrate.columns and col_9 in df_growthrate.columns:
        # Check if the student exists and if both 8th and 9th marks are not NaN
        condition = df_growthrate[col_8].notna() & df_growthrate[col_9].notna()
        growth_8_to_9[f"{subject}_Growth_{year}_to_{next_year}"] = np.where(
            condition, df_growthrate[col_9] - df_growthrate[col_8], 0  # Default to 0 if marks are missing
        )
    else:
        growth_8_to_9[f"{subject}_Growth_{year}_to_{next_year}"] = 0  # Default to 0 if columns are missing

# Create DataFrame for the growth calculations
growth_8_to_9_df = pd.DataFrame(growth_8_to_9)

# Save the growth to CSV file
#growth_8_to_9_df.to_csv("Growth_8_to_9.csv", index=False)

# Output the processed growth data (for debugging or inspection)
print("Growth 8th to 9th:")
print(growth_8_to_9_df)