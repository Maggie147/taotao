import pandas as pd

lst = [
    ['A','x',0],
    ['B','x',0],
    ['A','x',0],
    ['B','y',0],
]

df = pd.DataFrame(lst)

print(df)
df[2] = df.apply(lambda x: map(int, df[(df[0]==x[0])&(df[1]==x[1])].count() <= 1), axis=1)
print(df)

print(type(df))