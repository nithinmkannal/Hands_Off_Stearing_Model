import pandas as pd
import numpy as np
df=pd.read_csv("trainingexamples.csv")
n=6
a=[]
for i in range(len(df)):
    a.append(df.iloc[i].to_list)
print(a)
hypo=[]
for i in range(len(df)):
    if a[i][n]=="Y":
    