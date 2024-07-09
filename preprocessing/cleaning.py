import pandas as pd
import numpy as np
import json
import os
print(os.getcwd())

data = pd.read_json("data/final_dataset.json")


df = pd.DataFrame(data)
data_csv1 = df.to_csv("data/dataset1.csv")

df.columns

print(df.head())
print("Done!")
