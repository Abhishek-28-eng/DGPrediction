import pandas as pd
import numpy as np
import seaborn as sns
import sys
import os
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score,classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn.ensemble import VotingClassifier, RandomForestClassifier
from xgboost import XGBClassifier
sys.path.append('./Database')
import fifthdb
import sixthdb
import seventhdb
import eightdb
import ninethdb
import tenthdb


# Load the data for each standard
scores_5th = fifthdb.fifth_std
scores_6th = sixthdb.sixth_std
scores_7th = seventhdb.seventh_std
scores_8th = eightdb.eight_std
scores_9th = ninethdb.nineth_std
scores_10th = tenthdb.tenth_std

# Rename columns to include the year for easier merging
scores_5th = scores_5th.add_suffix("_5").rename(columns={"Student_id_5": "Student_id"})
scores_6th = scores_6th.add_suffix("_6").rename(columns={"Student_id_6": "Student_id"})
scores_7th = scores_7th.add_suffix("_7").rename(columns={"Student_id_7": "Student_id"})
scores_8th = scores_8th.add_suffix("_8").rename(columns={"Student_id_8": "Student_id"})
scores_9th = scores_9th.add_suffix("_9").rename(columns={"Student_id_9": "Student_id"})
scores_10th = scores_10th.add_suffix("_10").rename(columns={"Student_id_10": "Student_id"})

# Merge datasets on Unique_ID
df_growthrate = scores_5th.merge(scores_6th, on="Student_id") \
               .merge(scores_7th, on="Student_id") \
               .merge(scores_8th, on="Student_id") \
               .merge(scores_9th, on="Student_id") \
               .merge(scores_10th, on="Student_id")
df_growthrate
# df_growthrate=pd.DataFrame(df_growthrate)
# df_growthrate.to_csv("testing.csv", index=False)
# df_growthrate = df_growthrate.drop(columns=["Interest_5", "Interest_6", "Interest_7", "Interest_8", "Interest_9", "Interest_10"])
# df_growthrate

