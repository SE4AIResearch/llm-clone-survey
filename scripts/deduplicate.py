import pandas as pd
from Levenshtein import distance
THRESHOLD = 5

df = pd.read_csv('new_data.csv')
df = df[['cited_by', 'Title']]
df['Title'] = df['Title'].astype(str)

for paper in df['Title']:
    firstChar = paper[0]
    if firstChar.isdigit():
        index = paper.find('.')
        paper = paper[index+2:]
    elif firstChar == '[':
        index = paper.find(']')
        paper = paper[index+2:]

df = df.drop_duplicates(subset=['Title'])

f = open("duplicates.txt", "w")


for paper in range(len(df['Title'])):
    for compare in range(len(df['Title'])):
        if paper != compare:
                edit_distance = distance(df.iloc[paper,1], df.iloc[compare,1])
                if edit_distance <= THRESHOLD:
                    f.write("POSSIBLE DUPLICATES")
                    og = str(paper) + " " + df.iloc[paper,1]
                    compare = str(compare) + " " + df.iloc[compare,1]
                    f.write(og)
                    f.write(compare)
                    f.write('\n')
                    print('found')



f.close()