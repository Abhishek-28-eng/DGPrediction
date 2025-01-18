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

subjects_5_to_8 = ["Marathi", "Urdu", "Hindi", "English", "History", "Science", 
                   "Geography", "Drawing", "Sports", "Environmental Studies", "Math", "Computer"]

year = 6
next_year = 7
growth_6_to_7 = {"Student_id": df_growthrate["Student_id"]}  # Start with Unique_ID
for subject in subjects_5_to_8:
    if f"{subject}_{year}" in df_growthrate.columns and f"{subject}_{next_year}" in df_growthrate.columns:
        condition = df_growthrate[f"{subject}_{year}"].notna() & df_growthrate[f"{subject}_{next_year}"].notna()
        growth_6_to_7[f"{subject}_Growth_{year}_to_{next_year}"] = np.where(
            condition, df_growthrate[f"{subject}_{next_year}"] - df_growthrate[f"{subject}_{year}"], np.nan
        )
    else:
        growth_6_to_7[f"{subject}_Growth_{year}_to_{next_year}"] = np.nan

growth_6_to_7_df = pd.DataFrame(growth_6_to_7)
#growth_5_to_6_df.to_csv("Growth_6_to_7.csv", index=False)
print("Growth 6th to 7th:")
#print(growth_6_to_7_df.head())
growth_6_to_7_df