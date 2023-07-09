import pandas as pd
import numpy as np
df=pd.read_csv("enjoysport.csv")

a=[]
for i in range(len(df)):
   a.append(df.iloc[i].to_list())
n=6
hypo=[]

for i in range(n):
   hypo.append(a[0][i])

for i in range(len(df)):
   if a[i][n]=="yes":
      for j in range(n):
         if a[i][j]!=hypo[j]:
            hypo[j]="?"
   print(f"the hypo of {i} attribute is {hypo}")

print("*"*70)
print(f"final hypo is {hypo}")

      